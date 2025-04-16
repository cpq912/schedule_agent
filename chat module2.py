import getpass
import os

# if not os.getenv("DEEPSEEK_API_KEY"):
#     os.environ["DEEPSEEK_API_KEY"] = getpass.getpass("Enter your DeepSeek API key: ")
import langchain_deepseek
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
from langchain.agents import OpenAIFunctionsAgent
from langchain.schema import SystemMessage
from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.schema import SystemMessage, HumanMessage
# Create Schedule Checker Agent

promt_content="""

Role: I am a scheduling assistant focused on understanding your calendar needs.

My task is to identify if you want to:
1. Add a new event
2. Check existing schedule
3. Modify an event
4. delete an event
 
I will respond with "User needs: (add/check/modify/delete)" followed by relevant questions.

Examples:
User: "I need to schedule a meeting tomorrow"
Response: "User needs: add"

User: "What's on my calendar for next week?"
Response: "User needs: check"

User: "Can you change the time of my dentist appointment?"
Response: "User needs: modify"
"""
chat_prompt = ChatPromptTemplate.from_messages([
    SystemMessage(content=promt_content),
    MessagesPlaceholder(variable_name="chat_history",optional=True),
    HumanMessage(content="{input}"),
     MessagesPlaceholder("agent_scratchpad")
])


chater = create_openai_functions_agent(llm,tools=[], prompt=chat_prompt )
chater_executor = AgentExecutor(
    agent=chater,
    tools=[],  # Add your tools here
    verbose=True,
    metadata={"agent_name": "chater"}
)

response =chater_executor.invoke({"input": "what do i need to do next week"})


# Uncomment and modify the messages list for chat history
time="2025-2-25 21:00"
chat_init = [
    ("system", f'''

Role: I am a scheduling assistant focused on understanding your calendar needs.

My task is to identify if you want to:
1. Add a new event
2. Check existing schedule
3. Modify an event
4. delete an event
5. Add a periodic event

The period phrase could be like this (could be more than this):
"Every week" 
"Every 10 days" 
"Twice a month" 
"every Mon/Wed/Fri"



Output:
I will respond with "User needs: (add/check/modify/delete/period)".
no other words are allowed
Strictly follow the following format:

Examples:
User: "I need to schedule a meeting tomorrow"
Response: "User needs: add"

User: "What's on my calendar for next week?"
Response: "User needs: check"

User: "Can you change the time of my dentist appointment?"
Response: "User needs: modify"

User: "I want to study for 8 hours every week"
Response: "User needs: period"
''')
]


c_messages=chat_init
c_messages.append(("human", 'cancel it  '))

def type_agent(agenttype,message,llm):
    response = llm.invoke(message)
    return f"[{agenttype}]: {response.content}"

c_ai_msg=type_agent("chater",c_messages,llm)
#c_ai_msg = llm.invoke(c_messages)
print(f"\nAI: {c_ai_msg}")


c_messages.append(("ai", ai_msg.content))

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

completion = client.chat.completions.create(
    model="qwen2.5-7b-instruct", # This example uses qwen-plus. You can change the model name as needed. Model list: https://www.alibabacloud.com/help/en/model-studio/getting-started/models
    messages=[
        {'role': 'system', 'content': chat_init[0][1]},
        {'role': 'user', 'content': 'i need to workout 3 times a week'}],
)
    
#print(completion.model_dump_json()['messages']['content'])
print(completion.choices[0].message.content)





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
