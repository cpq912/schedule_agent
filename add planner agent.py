#this agent will accept needs from extractor when the information is not complete
#it will generate a plan based on existed event and user needs
#it shold always ground the planner before writing to database


import getpass
import os

# if not os.getenv("DEEPSEEK_API_KEY"):
#     os.environ["DEEPSEEK_API_KEY"] = getpass.getpass("Enter your DeepSeek API key: ")

from langchain_deepseek import ChatDeepSeek

llm = ChatDeepSeek(
    model="deepseek-chat",
    temperature=0,
    max_tokens=5000,
    timeout=60,
    max_retries=2,
    api_key="sk-dba351629c004c41b3c4c99c9e806db4"
    # other params...
)

# Uncomment and modify the messages list for chat history
time="2025-2-25 21:00"
chat_init = [
    ("system", f"""Role: I am a Schedule Planning Specialist that optimizes event scheduling.
    I need to follow the rules strictly.

Input:
- Existing Events: Current scheduled events list
- New Requirements: Events to be scheduled (may have missing fields)
- User Preferences: Optional scheduling preferences

Process:
1. For incomplete events, I will:
   - Set default meeting duration: 1 hour
   - Assign appropriate priority (1-5)
   - Consider category-based optimal timing

2. For scheduling, I will:
   - Avoid time conflicts
   - Follow scheduling best practices
   - Consider event categories and priorities

Output Format:
Suggested Schedule:
(below should be a list of new scheduled event [{{}},{{}}])
{{
    "event_id": [original],
    "start_time": [original or suggested],
    "end_time": [original or suggested],
    "category": [original],
    "description": [original],
    "priority": [original or suggested]
}}


Would this schedule work for you?"

Conflict explaination:
Only explain why you give the suggestion when you found conflict, and only explain about the conflict using event names or descriptions,
do not use event id ,do not include others.

After user feedback:
- If changes needed: Provide new suggestion
- If confirmed: Output final format:
status: confirmed
plan: {{final schedule details}}

Your input is listed here:
existed_events:{feteched_data}, 
new_requirement:{new_data},
 user preference:

rules:
1.if no conflict found, do not explain conflict in the output.
2.if the users change the existed events, then the existed events will be consider new scheduled showing in output.
"""
)
]

import json
with open('history event list.json', 'r', encoding='utf-8') as file:
    feteched_data = json.load(file)

#user_feedback="not provided"

new_data=[
  { "event_id": "asdw3ee1",
    "start_time": "2025-03-03 9:30",
    "end_time": "", 
    "category": "Work",
    "description": "Meeting",
    "priority": "5"
  },
  { "event_id": "ass35ee1",
    "start_time": "2025-03-04 16:00",
    "end_time": "2025-03-04 18:00",
    "category": "Work",
    "description": "Meeting",
    "priority": ""
  }
  ]




c_messages=chat_init

c_ai_msg = llm.invoke(c_messages)
print(f"\nAI: {c_ai_msg.content}")


c_messages.append(("ai", c_ai_msg.content))

c_messages.append(("human", 'no i will change the old event to 2pm'))


while True:
    user_input = input("\nYou: ")
    if user_input.lower() == 'end':
        break
    # Add user message to history and get AI response
    messages.append(("human", user_input))
    try:
        ai_msg = llm.invoke(messages)
        messages.append(("ai", ai_msg.content))
        print(f"\nAI: {ai_msg.content}")
    except Exception as e:
        print(f"\nError: {str(e)}")
        break



json.loads(c_ai_msg.content.split("Suggested Schedule:")[1].split("Would this")[0].strip())


c_ai_msg.content.split("Conflict explanation:")[1].split("Would this")[0].strip()