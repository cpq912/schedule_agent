#this agent will extract user intention about the new event infor based on existed event and the instruction message
#missing data assume to be the same of the old data 

import getpass
import os

# if not os.getenv("DEEPSEEK_API_KEY"):
#     os.environ["DEEPSEEK_API_KEY"] = getpass.getpass("Enter your DeepSeek API key: ")

from langchain_deepseek import ChatDeepSeek

llm = ChatDeepSeek(
    model="deepseek-chat",
    temperature=0,
    max_tokens=5000,
    timeout=30,
    max_retries=2,
    api_key="sk-dba351629c004c41b3c4c99c9e806db4"
    # other params...
)

# Uncomment and modify the messages list for chat history
time="2025-3-13 21:00"
user_instruction="change tommorow meeting priority to 1"
origin_event={
    "event_id": "223efwe", 
    "start_time": "20250314 12:00", 
    "end_time": "20250314 14:00",   
    "category": "Work",
    "description": "meeting",
    "priority": "4"

}

chat_init = [
    ("system", f"""
Role: I am an Event Modification Agent. My task is to:

When the user requests to modify an event, generate a new JSON event plan by updating the original 
event with the user’s instructions. Follow these rules:

1.Input Format:
User provides a modification request (e.g., "Change tomorrow’s meeting to 4pm").
Original event is provided in JSON format
{{
    "event_id": "random_alphanumeric", 
    "start_time": "YYYY-MM-DD HH:MM", 
    "end_time": "YYYY-MM-DD HH:MM",   
    "category": "Work/Personal/Health",
    "description": "user input",
    "priority": "1-5"
}}
2.work flow:
Identify Changes: Extract only the fields the user explicitly modifies (e.g., time, description, priority).
Retain Unchanged Fields: Keep all other fields from the original event unchanged.
Time Logic:
Convert relative times (e.g., "tomorrow") to absolute dates using the original event’s date as context.
Adjust end_time automatically if duration is implied (e.g., "Change meeting to 4pm" → end_time shifts by the same duration).
Validation: Ensure start_time < end_time. If conflicting, ask the user to clarify.

3.Output:
Output only the JSON with updated infor, if there are many event json, put them is a list


content:
current time is :{time}
the user instruction is : {user_instruction}
the origin event is :{origin_event}

"""
)
]


c_messages=chat_init
c_messages.append(("human", 'no you can help me do it'))
c_ai_msg = llm.invoke(c_messages)
print(f"\nAI: {c_ai_msg.content}")

c_messages.append(("ai", c_ai_msg.content))

messages.append(("ai", 'Downstream agent: the date you check has no event'))


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
