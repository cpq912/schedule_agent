#this agent will handle periodic events schedule

from langchain_deepseek import ChatDeepSeek

llm = ChatDeepSeek(
    model="deepseek-chat",
    temperature=0,
    max_tokens=8000,
    timeout=60,
    max_retries=2,
    api_key="sk-dba351629c004c41b3c4c99c9e806db4"
    # other params...
)



# Uncomment and modify the messages list for chat history
time="2025-2-25 21:00"

new_todo=[
{"id":"sdffasf12","content":"do gym three times a week","stat":"unprocessed"}]
#{"id":"ss34da123","content":"running every saturday 7:00","stat":"unprocessed"},
#{"id":"rknava123","content":"read papers 1 hour every day","stat":"unprocessed"}

## add new todo


## delete todo 

