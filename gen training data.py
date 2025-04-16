import getpass
import os
import json
import random
import uuid
import datetime
from typing import List, Dict, Any, Optional, Tuple

# if not os.getenv("DEEPSEEK_API_KEY"):
#     os.environ["DEEPSEEK_API_KEY"] = getpass.getpass("Enter your DeepSeek API key: ")

from langchain_deepseek import ChatDeepSeek

llm = ChatDeepSeek(
    model="deepseek-chat",
    temperature=0.7,  # Using higher temperature for more diverse outputs
    max_tokens=8000,
    timeout=180,
    max_retries=2,
    api_key="sk-dba351629c004c41b3c4c99c9e806db4"
    # other params...
)

# Set the current time for reference
current_time = datetime.datetime(2025, 3, 1, 21, 0)  # 2025-02-25 21:00

# System prompts for generating training data
# System prompt for Round 1 examples
system_prompt_round1 = """
You are a data generator for training an event information collector LLM. 
Your task is to create realistic and diverse examples of user inputs about scheduling events and the corresponding model outputs for ROUND 1 ONLY.

Each example should include:
1. A user input requesting to schedule an event (can be work meetings, personal appointments, health checkups, etc.)
2. The expected model output in three parts:
   - Part 1: Extraction of explicit information from user input (ONLY what is explicitly provided, use null for missing fields)
   - Part 2: Inference for missing fields
   - Part 3: Formatted JSON output

The current reference time is {time} Saturday.

Create {num_examples} diverse examples with the following variations:
- Different event types (work, personal, health)
- Different time expressions (specific times, relative times like "tomorrow", "next week")
- Different levels of detail in user input (some with missing fields)

MAKE USER INPUTS HIGHLY DIVERSE:
- Use various ways to express scheduling needs ("I need to...", "Can you add...", "Please schedule...", etc.)
- Include different event descriptions (meetings, doctor appointments, family gatherings, workouts, etc.)
- Vary the amount of detail provided (some with complete info, others with minimal details)
- Use different time expressions ("next Monday at 3", "tomorrow afternoon", "on the 15th", etc.)
- Include different priorities and categories when mentioned

Round 1 Rules:
- Include a "round" field with value 1
- In part1_extraction, ONLY include information explicitly provided in the user input
- If information is not explicitly provided, use null for that field
- Add a "follow_up" field in part3_formatted ONLY if there are null values in part1_extraction
- The follow_up should ONLY ask about the missing fields using EXACTLY this format: "do you want to provide more detail about [missing_fields]" where [missing_fields] is a list of the fields with null values
- If there are no null values in part1_extraction, set follow_up to empty string ""
- Make sure some examples have intentionally missing fields to prompt follow-up questions

Follow this exact format for Round 1 examples:
```json
{{
  "round": 1,
  "user": "[User's request to schedule an event]",
  "assistant": {{
    "part1_extraction": {{
      "start_time": "[extracted or null]",
      "end_time": "[extracted or null]",
      "priority": "[extracted or null]",
      "category": "[extracted or null]",
      "description": "[extracted or null]"
    }},
    "part2_inference": {{
      "time_reasoning": "[explanation of time inference]",
      "end_time_calculation": "[explanation of duration inference]",
      "priority_analysis": "[explanation of priority inference]",
      "category_logic": "[explanation of category inference]"
    }},
    "part3_formatted": {{
      "event_id": "[random ID]",
      "start_time": "YYYY-MM-DD HH:MM",
      "end_time": "YYYY-MM-DD HH:MM",
      "priority": [1-5],
      "category": "[Work/Personal/Health]",
      "description": "[event description]",
      "follow_up": "do you want to provide more detail about [missing_fields]"
    }}
  }}
}}
```

Make sure the examples are diverse and realistic.
"""

# System prompt for Round 2 examples
system_prompt_round2 = """
You are a data generator for training an event information collector LLM. 
Your task is to create realistic and diverse examples of user inputs about scheduling events and the corresponding model outputs for ROUND 2 ONLY.

Each example should include:
1. The complete Round 1 context (user request and model response)
2. A Round 2 user response providing missing information
3. The expected model output in three parts:
   - Part 1: Extraction of explicit information from user input (ONLY what is explicitly provided, use null for missing fields)
   - Part 2: Inference for missing fields
   - Part 3: Formatted JSON output

The current reference time is {time} Saturday.

Create {num_examples} diverse examples with the following variations:
- Different event types (work, personal, health)
- Different time expressions (specific times, relative times like "tomorrow", "next week")
- Different levels of detail in user input (some with missing fields)

MAKE USER INPUTS HIGHLY DIVERSE:
- Use various ways to express scheduling needs ("I need to...", "Can you add...", "Please schedule...", etc.)
- Include different event descriptions (meetings, doctor appointments, family gatherings, workouts, etc.)
- Vary the amount of detail provided (some with complete info, others with minimal details)
- Use different time expressions ("next Monday at 3", "tomorrow afternoon", "on the 15th", etc.)
- Include different priorities and categories when mentioned

Round 2 Rules:
- Include a "round" field with value 2
- Include the complete Round 1 context (user_input and model_output from Round 1)
- In Round 1 context, make sure the follow_up field uses the format: "do you want to provide more detail about [missing_fields]"
- Include the Round 2 user_input that responds to the follow-up question
- In part1_extraction, ONLY include information explicitly provided in the user input
- If information is not explicitly provided, use null for that field
- The part3_formatted should now be complete with all information

Follow this exact format for Round 2 examples:
```json
{{
  "round": 2,
  "round1_context": {{
    "user": "[Round 1 user request]",
    "assistant": {{
      "part1_extraction": {{
        "start_time": "[extracted or null]",
        "end_time": "[extracted or null]",
        "priority": "[extracted or null]",
        "category": "[extracted or null]",
        "description": "[extracted or null]"
      }},
      "part2_inference": {{
        "time_reasoning": "[explanation of time inference]",
        "end_time_calculation": "[explanation of duration inference]",
        "priority_analysis": "[explanation of priority inference]",
        "category_logic": "[explanation of category inference]"
      }},
      "part3_formatted": {{
        "event_id": "[random ID]",
        "start_time": "YYYY-MM-DD HH:MM",
        "end_time": "YYYY-MM-DD HH:MM",
        "priority": [1-5],
        "category": "[Work/Personal/Health]",
        "description": "[event description]",
        "follow_up": "do you want to provide more detail about [missing_fields]"
      }}
    }}
  }},
  "user": "[Round 2 user response with missing information]",
  "assistant": {{
    "part1_extraction": {{
      "start_time": "[extracted or null]",
      "end_time": "[extracted or null]",
      "priority": "[extracted or null]",
      "category": "[extracted or null]",
      "description": "[extracted or null]"
    }},
    "part2_inference": {{
      "time_reasoning": "[explanation of time inference]",
      "end_time_calculation": "[explanation of duration inference]",
      "priority_analysis": "[explanation of priority inference]",
      "category_logic": "[explanation of category inference]"
    }},
    "part3_formatted": {{
      "event_id": "[random ID]",
      "start_time": "YYYY-MM-DD HH:MM",
      "end_time": "YYYY-MM-DD HH:MM",
      "priority": [1-5],
      "category": "[Work/Personal/Health]",
      "description": "[event description]"
    }}
  }}
}}
```

Make sure the examples are diverse and realistic.
"""

# Combined system prompt (for backward compatibility)
system_prompt = system_prompt_round1

def generate_batch(batch_size: int = 10, round_type: int = 1) -> List[Dict[str, Any]]:
    """Generate a batch of training examples
    
    Args:
        batch_size: Number of examples to generate
        round_type: 1 for Round 1 examples, 2 for Round 2 examples
    """
    
    # Select the appropriate system prompt based on round_type
    if round_type == 1:
        prompt_template = system_prompt_round1
    elif round_type == 2:
        prompt_template = system_prompt_round2
    else:
        raise ValueError("round_type must be either 1 or 2")
    
    # Format the system prompt with current time and batch size
    formatted_prompt = prompt_template.format(time=current_time.strftime("%Y-%m-%d %H:%M"), num_examples=batch_size)
    
    # Initialize the chat with the system prompt
    messages = [("system", formatted_prompt)]
    messages.append(("human", f"Generate {batch_size} diverse training examples for the event information collector LLM for Round {round_type}."))
    
    # Get response from the LLM
    response = llm.invoke(messages)
    
    # Extract the JSON data from the response
    try:
        # Find all JSON objects in the response
        content = response.content
        # Clean up the response to extract valid JSON
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0]
        
        # Try to parse as a list first
        try:
            data = json.loads(f"[{content}]")
        except json.JSONDecodeError:
            # If that fails, try to find and parse individual JSON objects
            import re
            json_objects = re.findall(r'\{[^\{\}]*((\{[^\{\}]*\})[^\{\}]*)*\}', content)
            data = []
            for obj_match in json_objects:
                try:
                    obj = json.loads(obj_match[0])
                    data.append(obj)
                except json.JSONDecodeError:
                    continue
        
        print(f"Successfully parsed {len(data)} examples")
        return data
    except Exception as e:
        print(f"Error parsing JSON: {e}")
        print(f"Raw response: {response.content}")
        return []

def save_data(data: List[Dict[str, Any]], filename: str = "training_data.json"):
    """Save the generated data to a JSON file"""
    try:
        # Check if file exists and load existing data
        if os.path.exists(filename):
            with open(filename, 'r', encoding='utf-8') as f:
                existing_data = json.load(f)
        else:
            existing_data = []
        
        # Append new data
        existing_data.extend(data)
        
        # Save the combined data
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(existing_data, f, indent=2, ensure_ascii=False)
        
        print(f"Successfully saved {len(data)} examples. Total examples: {len(existing_data)}")
    except Exception as e:
        print(f"Error saving data: {e}")

def main(total_examples: int = 30, batch_size: int = 5):
    """Generate the specified number of training examples"""
    num_batches = total_examples // batch_size
    all_data = []
    
    # Generate Round 1 examples
    # print("Generating Round 1 examples...")
    # for i in range(num_batches):
    #     print(f"Generating Round 1 batch {i+1}/{num_batches}...")
    #     batch_data = generate_batch(batch_size, round_type=1)
    #     if batch_data:
    #         all_data.extend(batch_data)
    #         # Save incrementally to avoid losing data if the process is interrupted
    #         save_data(batch_data, "event_collector_training_data.json")
    #     else:
    #         print("Failed to generate batch, retrying...")
    #         i -= 1  # Retry this batch
    
    # Generate Round 2 examples
    print("\nGenerating Round 2 examples...")
    for i in range(num_batches):
        print(f"Generating Round 2 batch {i+1}/{num_batches}...")
        batch_data = generate_batch(batch_size, round_type=2)
        if batch_data:
            all_data.extend(batch_data)
            # Save incrementally to avoid losing data if the process is interrupted
            save_data(batch_data, "event_collector_training_data.json")
        else:
            print("Failed to generate batch, retrying...")
            i -= 1  # Retry this batch
    
    print(f"Data generation complete. Generated {len(all_data)} examples.")

if __name__ == "__main__":
    main(300, 5)
