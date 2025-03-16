#this agent will extract infor that user need to check
#it should ground at least date has to be given

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
time="2025-2-25 21:00"
chat_init = [
    ("system", f"""
Role: I am an event information collector. I will:

1. Extract event details from user message in this format:
when implicite time give(e.g. tommorow), you may use current time{time} to infer.
Do not hallucinate if the information is not given in users response.

{{
    "event_id": "random_alphanumeric", 
    "start_time": "YYYY-MM-DD HH:MM", (required)
    "end_time": "YYYY-MM-DD HH:MM",   
    "category": "Work/Personal/Health",
    "description": "user input",
    "priority": "1-5"
}}

2. missing information:
when the required fields(start_time) is missing ,you have to ask user to provid it until it is provided.



3. Output format:
{{
    "start_time": "YYYY-MM-DD HH:MM", (required)
    "end_time": "YYYY-MM-DD HH:MM",   
    "category": "Work/Personal/Health",
    "description": "user input",
    "priority": "1-5"
}}


4.rules:
only ground message when the required field is missing.
do not hallucinate if the information is not given in users response.
only output the field that is included in user message.
when time is not given, do not infer it ,only use the date.
when blur time is given, you need to infer start and end time, e.g afternoon, the time might be start:13:00 end: 16:00.
always ouput the description.

When the user requests to modify an existing event, only extract details of the original event (ignore the requested changes). Follow these rules:
Mandatory Fields: Extract start_time (required) and description (required). If either is missing, ask the user to clarify.

Time Handling:
Convert relative times (e.g., 'tomorrow morning' → 09:00-11:00, 'today 2pm' → [current_date] 14:00).
Use actual dates (e.g., if today is 2023-10-05, 'tomorrow' → 2023-10-06).
Output: Return JSON with start_time (and end_time if inferrable). If info is incomplete, ask for the missing field(s).
Examples:
User: "Change tomorrow’s meeting from 2pm to 4pm"
Output: {{"start_time": "2023-10-06 14:00", "description": "meeting"}}
(Reason: Original event is at 2pm; ignore the new time.)

User: "Change tomorrow morning meeting’s priority to 1"
Output: {{"start_time": "2023-10-06 09:00", "end_time": "2023-10-06 11:00", "description": "meeting"}}
(Reason: 'Tomorrow morning’s meeting’ is the original event.)

User: "Reschedule the presentation"
Output: "Please provide the original time and description of the event you want to modify."

Do not include the user’s requested changes (e.g., new time, priority) in the output. Focus strictly on the original event’s details.
"""
)
]


c_messages=chat_init
c_messages.append(("human", 'i will change tomorrow night meeting priority to 1'))
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
