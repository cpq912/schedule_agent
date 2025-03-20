#this agent is responsible for adding a new event to existed events
# it will ask user for one time if any fields missing and extract info about the event
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
Auto-infer category (Work/Personal/Health).
{{
    "event_id": "random_alphanumeric", 
    "start_time": "YYYY-MM-DD HH:MM", (required)
    "end_time": "YYYY-MM-DD HH:MM",   
    "category": "Work/Personal/Health",
    "description": "user input",
    "priority": "1-5"
}}

2. 
grounded message: "your grounded message"
when fields are missing:
- First Response: respond with "Would you provide more information about [list missing fields]?"
- Second Response: "Since you haven't given all info, I shall try it based on your preference"

When all fields provided: "Ok, I shall help you arrange it"


If any field is missing, you may ground "would you provide more information about (missing fileds) ?"
If you all field is provided, you may ground "ok i shall help you arrange it "
If after your inquire the fields are still missing , you may ground "since you haven't give all info, i shall try it based on your preference " 


3. Output format:
turns:1-2(this is showing the number of turns that you are anwsering)
Status: completed/partially completed
grounded message: "your grounded message"
Collected events: [list of events in JSON format]


Example:
User: "Schedule a meeting tomorrow at 2pm"
Response: "I need the following details:
- Meeting duration/end time
- Priority (1-5)
- Category (Work/Personal/Health)

Status: partially completed
Events: {{
    "event_id": "mt123xyz",
    "start_time": "2025-02-26 14:00",
    "description": "meeting"
}}"


"""
)
]


c_messages=chat_init
c_messages.append(("human", 'i will swim tommorrow at 10:00 for 2 hours, priority 3, healthy'))
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


def extract_message(response, field):
    # Find the grounded message between quotes
    if field in response:
        # Split by grounded message: and get the part after it
        message_part = response.split(field)[1].strip()
        # Extract content between quotes
        try:
            message = message_part.split('"')[1]
            return message
        except IndexError:
            return None
    return None

extract_message(c_ai_msg.content,"Collected events:")


#json.loads(c_ai_msg.content.split("```json")[1].strip().split("```")[0].strip())


#"message" in c_ai_msg.content


c_ai_msg.content.split("Collected events:")[1].strip()