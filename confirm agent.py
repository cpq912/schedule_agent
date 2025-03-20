#this agent is able to sense the user is agree to the plan or not, could be adpate by a model

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

inti=[(
'system',"""
role:
you are a sensitive agent that good at judging the user's agreement to the plan.

output:
if the user agree, return "agree"
if the user disagree, return "disagree"
if the user is using a statement, not showing any intention, return "none"

this is user input:{user_input}
"""


)]

messages= inti
messages.append(("human", 'i need to swim tommorrow'))
ai_msg = llm.invoke(messages)
print(f"\nAI: {ai_msg.content}")