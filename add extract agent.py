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
time="2025-2-25 21:00 Tuesday"
chat_init = [
    ("system", f"""
Role: I am an event information collector. I will:

1. Extract event details from user message in this event format:
when implicite time give(e.g. tommorow), you may use current time{time} to infer.
Do not hallucinate if the information is not given in users response.
If information is not provided in user message, the corresponding item should not existed.
Auto-infer and fill category item only (Work/Personal/Health).
You should auto gen an eventid over 20 digits that impossible to repeat
{{
    "event_id": "random_alphanumeric", 
    "start_time": "YYYY-MM-DD HH:MM", 
    "end_time": "YYYY-MM-DD HH:MM",   
    "category": "Work/Personal/Health",
    "description": "user input",
    "priority": "1-5"
}}




2.Missing field identify:
Compare your extracted information json to the event format (fields include start_time,end_time,category,description, priority), identify which fields are missing


3. Grounding process:
If identify missing information,you need to aks user to provided it by: "Would you provide more information about [list missing fields]?"

After user reply,use user reply to update the extracted information, then decide :
(1)if every filed is complete, reply :"Ok, I shall help you arrange it"
(2)if every filed is not complete, reply "Since you haven't given all info, I shall try it based on your preference"

Rule:
1.Only update the extracted information with the information user provided(except category could be infer by you ), do not infer and add to the field.


4. Output format:
1.turns:1-2(this is showing the number of turns that you are anwsering)
2.Reasoning:(the reason process how you get the final collected events)
3.Status: completed/partially completed
4.grounded message: "your grounded message"
5.Collected events: list of newly scheduled events [{{}},{{}}]

output rules:
1.YOU MUST STRICTLY FOLLOW THE OUTPUT FORMAT
2.DO NOT ADD WORDS BEFORE OR AFTER THE 4 OUPUTPARTS
3.Do not add space after ":", (turns:1 is valid)(turns: 1 is invalid)

Valid format example:
turns:1
Status:completed
grounded message:would you provide more information about end_time?
Collected events:[{{"event_id":"123456789012345678901","start_time":"2024-02-26 14:00","end_time":"2024-02-26 15:00","description":"meeting","priority":"5"}}]

invalid format example:
Collected events:[{{"event_id":"123456789012345678901","start_time":"2024-02-26 14:00","end_time":"2024-02-26 15:00","description":"meeting","priority":"5"}}] tell me if you need more help

5.Rules:
1.At most you can response two times, first time the turns=1, second time the turns=2
2.After first response, no matter user provide more information or not, you should not repeat ask for more information.

"""
)
]


c_messages=chat_init
c_messages.append(("human", 'i will swim tommorrow at 10:00 for 2 hours, priority 3, healthy'))
c_ai_msg = llm.invoke(c_messages)
print(f"\nAI: {c_ai_msg.content}")

c_messages.append(("ai", c_ai_msg.content))

messages.append(("ai", 'Downstream agent: the date you check has no event'))





#test qwen performance
import os
from openai import OpenAI
import json
client = OpenAI(
    # If environment variables are not configured, replace the following line with: api_key="sk-xxx",
    api_key="sk-d0d414ae60c04b569db14cd502eeb8bc", 
    base_url="https://dashscope-intl.aliyuncs.com/compatible-mode/v1",
)


sysprompt="""
you are a event information collector. you will follow the steps below:

1.extract  start_time, end_time,priority, category,description of the event from user input
- if related time given, you may use current time to infer. 
(example: user:i will swim next Friday , if current time is 2025-2-25 Tuesday, next Friday should be 2025-2-28 )
-Note: the current time is  {time}, infer based on this time 
- the format for start_time and end_time is YYYY-MM-DD HH:MM

2.identify which fields are missing start_time, end_time,priority, category,description, show them in a list

3.you may infer priority (1-5, 1 is most important), category(Work/Personal/Health) and description by your self
- you may infer the end_time given start_time and possible period of this event

4.show the information collected in a json format

"""

completion = client.chat.completions.create(
    model="qwen2.5-7b-instruct", # This example uses qwen-plus. You can change the model name as needed. Model list: https://www.alibabacloud.com/help/en/model-studio/getting-started/models
    messages=[
        {'role':'system', 'content': sysprompt},
        {'role': 'user', 'content': 'i will swim next Monday  at 9pm  '}],
  
)
    
#print(completion.model_dump_json()['messages']['content'])
print(completion.choices[0].message.content)

history=completion.choices[0].message.content
completion = client.chat.completions.create(
    model="qwen2.5-7b-instruct", # This example uses qwen-plus. You can change the model name as needed. Model list: https://www.alibabacloud.com/help/en/model-studio/getting-started/models
    messages=[
        {'role': 'system', 'content': chat_init[0][1]},
        {'role': 'user', 'content': 'i will swim tommorrow at 9pm' },
        {'role': 'assistant', 'content': history },
        {'role': 'user', 'content': 'you can arrange it '}],
)
print(completion.choices[0].message.content)




time_infer_prompt=f"""

you should get the start_time from user input.
if the start_time is given in a related form ,you need to infer based on current time.
Do this step by step:
1.decide how many days after current time the event will start
2.attain the date by computing with current time and the days after current time
3.make sure you do not omit a single day

(example: user:i will swim next Friday , if current time is 2025-2-25 Tuesday, next Friday should be 2025-2-28 )

-Note: the current time is  {time}, infer based on this time 
- the format for start_time  is YYYY-MM-DD HH:MM
- you should be aware that Feburary has 28 days in 2025.

output format(strickly follow the format):

reason:
your inferering process

Output:
YYYY-MM-DD HH:MM  (if day and time given)
YYYY-MM-DD  (if day is given and time is not given)
none  (if day and time not given)

"""

completion = client.chat.completions.create(
    model="qwen2.5-14b-instruct", # This example uses qwen-plus. You can change the model name as needed. Model list: https://www.alibabacloud.com/help/en/model-studio/getting-started/models
    messages=[
        {'role':'system', 'content': time_infer_prompt},
        {'role': 'user', 'content': 'i will swim next saturday at 9pm'}],
  
)
    
#print(completion.model_dump_json()['messages']['content'])
start_time = completion.choices[0].message.content.split('Output:')[1].strip()




extracted_prompt=f"""


you are a event information collector. you will follow the steps below:

the event fields include :  start_time,end_time,time span,priority,category,description
1.extract  information of the event from user input
- note the start_time is this {start_time}.
- you could infer this event description if user do not provide description.

2.identify which fields are missing (start_time, end_time,priority, category)show them in a list


output format(strickly follow the format below)

reasoning: your reasoning process

output:
extracted infomation: only list all the provided  information and description
missing_fields:[list of missing fields]

"""


completion = client.chat.completions.create(
    model="qwen2.5-7b-instruct", # This example uses qwen-plus. You can change the model name as needed. Model list: https://www.alibabacloud.com/help/en/model-studio/getting-started/models
    messages=[
        {'role':'system', 'content': extracted_prompt},
        {'role': 'user', 'content': 'i will swim next saturday at 9pm, 2 hours,priority 1'}],
  
)

extracted_hist = completion.choices[0].message.content.split('output:')[1].strip()



autofill_prompt=f"""


you are a event information collector. you will follow the steps below:

1.infer and fill the missing fields given extracted information , user provided information and missing information
-inference guides:
-you may infer priority (1-5, 1 is most important), category(Work/Personal/Health) and description by your self
- you may infer the end_time given start_time and possible period of this event
2.combine all the information and output the result

the extracted information is this:{extracted_hist}

the event infor includes this :
{{
    "start_time": "YYYY-MM-DD HH:MM", 
    "end_time": "YYYY-MM-DD HH:MM",   
    "category": "Work/Personal/Health",
    "description": "user input",
    "priority": "1-5"
}}


output format(strickly follow the format below)

output:
reasoning: your reasoning process

Collected events:list of newly scheduled events [{{}},{{}}]
(e.g [{{"start_time":"2024-02-26 14:00","end_time":"2024-02-26 15:00","description":"meeting","priority":"5"}}] )


"""

completion = client.chat.completions.create(
    model="qwen2.5-7b-instruct", # This example uses qwen-plus. You can change the model name as needed. Model list: https://www.alibabacloud.com/help/en/model-studio/getting-started/models
    messages=[
        {'role':'system', 'content': autofill_prompt},
        {'role': 'user', 'content': 'no'}],
  
)

print(completion.choices[0].message.content)





added_list= json.loads(completion.choices[0].message.content.split('Collected events:')[1].strip())

import random
db=EventDatabase()
import string
write_event(added_list,'usersample222')


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