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
messages = [
    ("system", "You are ChronoGuide, an AI-powered temporal optimization \
     specialist. Your primary function is to analyze,\
      organize, and enhance human schedules through intelligent time orchestration, \
     ensuring optimal alignment between planned activities and actual temporal resources."),
]
#pure stack messages as memory
# messages.append(("human", "hi i'm want workout everyweek"))
# ai_msg = llm.invoke(messages)
# print(f"\nAI: {ai_msg.content}")

# while True:
#     user_input = input("\nYou: ")
#     if user_input.lower() == 'end':
#         break
#     # Add user message to history and get AI response
#     messages.append(("human", user_input))
#     try:
#         ai_msg = llm.invoke(messages)
#         messages.append(("ai", ai_msg.content))
#         print(f"\nAI: {ai_msg.content}")
#     except Exception as e:
#         print(f"\nError: {str(e)}")
#         break

#multiturn chat

chat=  ChatDeepSeek(
    model="deepseek-chat",
    temperature=0,
    max_tokens=200,
    timeout=30,
    max_retries=2,
    api_key="sk-dba351629c004c41b3c4c99c9e806db4"
    # other params...
)

#add memory with chain

# from langchain_core.messages import AIMessage, HumanMessage
# from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
# prompt = ChatPromptTemplate.from_messages(
#     [
#         (
#             "system",
#             "You are a helpful assistant. Answer all questions to the best of your ability.",
#         ),
#         MessagesPlaceholder(variable_name="chat_history"),
#         ("human", "{input}"),
#     ]
# )

# chain = prompt | chat
# from langchain.memory import ChatMessageHistory

# from langchain_core.runnables.history import RunnableWithMessageHistory

# demo_ephemeral_chat_history_for_chain = ChatMessageHistory()

# chain_with_message_history = RunnableWithMessageHistory(
#     chain,
#     lambda session_id: demo_ephemeral_chat_history_for_chain,
#     input_messages_key="input",
#     history_messages_key="chat_history",
# )

# chain_with_message_history.invoke(
#     {"input": "Translate this sentence from English to French: I love programming."},
#     {"configurable": {"session_id": "unused"}},
# )


# #external memory raw text 
# from langchain_mongodb.chat_message_histories import MongoDBChatMessageHistory

# chat_message_history = MongoDBChatMessageHistory(
#     session_id="test_session",
#     connection_string="mongodb+srv://chrispeng912:hdKhfSgWYWSCcqvf@agent.aosmv.mongodb.net/?retryWrites=true&w=majority&appName=agent",
#     database_name="my_db",
#     collection_name="chat_histories",
# )

# chat_message_history.add_user_message("I'm going to hongkong at 8pm")
# chat_message_history.add_ai_message("ok, i setup a note for you ")

# external memory embeddings
# sourece:https://python.langchain.com/docs/integrations/vectorstores/mongodb_atlas/#initialization
# https://python.langchain.com/docs/integrations/memory/mongodb_chat_message_history/
# from langchain_openai import OpenAIEmbeddings
# from langchain_community.embeddings import HuggingFaceEmbeddings

# embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")  # 这是一个轻量级且效果不错的模型

# # embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

# from langchain_mongodb import MongoDBAtlasVectorSearch
# from pymongo import MongoClient

# # initialize MongoDB python client
# client = MongoClient("mongodb+srv://chrispeng912:hdKhfSgWYWSCcqvf@agent.aosmv.mongodb.net/?retryWrites=true&w=majority&appName=agent")

# DB_NAME = "test_vector_db"
# COLLECTION_NAME = "langchain_test_vectorstores"
# ATLAS_VECTOR_SEARCH_INDEX_NAME = "langchain-test-index-vectorstores3"

# MONGODB_COLLECTION = client[DB_NAME][COLLECTION_NAME]

# vector_store = MongoDBAtlasVectorSearch(
#     collection=MONGODB_COLLECTION,
#     embedding=embeddings,
#     index_name=ATLAS_VECTOR_SEARCH_INDEX_NAME,
#     relevance_score_fn="cosine",
# )

# # Create vector search index on the collection
# # Since we are using the default OpenAI embedding model (ada-v2) we need to specify the dimensions as 1536
# # !!! this dims will vary to embedding models
# vector_store.create_vector_search_index(dimensions=384)


# from langchain_core.documents import Document

# document_1 = Document(
#     page_content="I had chocalate chip pancakes and scrambled eggs for breakfast this morning.",
#     metadata={"source": "tweet"},
# )
# document_2 = Document(
#     page_content="The weather forecast for tomorrow is cloudy and overcast, with a high of 62 degrees.",
#     metadata={"source": "news"},
# )

# documents = [
#     document_1,
#     document_2
# ]
# uuids=['1','2']
# vector_store.add_documents(documents=documents, ids=uuids)


# retriever = vector_store.as_retriever(
#     search_type="similarity_score_threshold",
#     search_kwargs={"k": 1, "score_threshold": 0.2},
# )
# retriever.invoke("what did i eat for breakfast")


# from pymongo import MongoClient

# 替换为你的连接字符串
# connection_string = "mongodb+srv://chrispeng912:hdKhfSgWYWSCcqvf@agent.aosmv.mongodb.net/?retryWrites=true&w=majority&appName=agent"

# try:
#     client = MongoClient(connection_string)
#     db = client.my_db
#     db.chat_histories.insert_one({"test": "connection"})
#     print("连接成功！")
# except Exception as e:
#     print(f"连接失败: {e}")



# reflection
# https://github.com/langchain-ai/langgraph/blob/main/docs/docs/tutorials/reflexion/reflexion.ipynb
from langchain_core.prompts import ChatPromptTemplate,MessagesPlaceholder
from langchain_core.messages import AIMessage, HumanMessage
prompt=ChatPromptTemplate.from_messages(
[
("system",
 "You are an essay asistant tasked with writing essays")
,
MessagesPlaceholder(variable_name="messages")
]
)

generate=prompt|llm

essay=""
request=HumanMessage(
    content="write an essy on dragon"
)

essay=generate.invoke([request]).content


for chunk in generate.stream({"messages": [request]}):
    print(chunk.content, end="")
   


reflection_promt=ChatPromptTemplate.from_messages(
[
("system",
 "You are a teacher grading an essay. generate critique and recommendation")
,
MessagesPlaceholder(variable_name="messages")
]
)

reflect= reflection_promt|llm

reflection=reflect.invoke([HumanMessage(essay)]).content

generate.invoke([request,AIMessage(essay),HumanMessage(reflection)]).content

#if not use langgraph, just define a generator and a reflection, and ask these two roles to work one after each other
# append alll the messages
#also pay attention to the message type, for generator, writing is AI, for reflection writing is human
print(essay)


from typing import Annotated, List, Sequence
from langgraph.graph import END, StateGraph, START
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import MemorySaver
from typing_extensions import TypedDict


class State(TypedDict):
    messages: Annotated[list, add_messages] #定义message是一个list，add_messages会在生成后自动在历史中追加而不是覆盖


async def generation_node(state: State) -> State:# 返回state
    return {"messages": [await generate.ainvoke(state["messages"])]}

#这里做了角色互换，（node要生成的都是ai）
#对写手来说，写作是ai，反馈是human
#对评级来说，写作是human，反馈是ai
async def reflection_node(state: State) -> State:
    # Other messages we need to adjust
    cls_map = {"ai": HumanMessage, "human": AIMessage}
    # First message is the original user request. We hold it the same for all nodes
    translated = [state["messages"][0]] + [
        cls_map[msg.type](content=msg.content) for msg in state["messages"][1:]
    ]
    res = await reflect.ainvoke(translated)
    # We treat the output of this as human feedback for the generator
    return {"messages": [HumanMessage(content=res.content)]}


builder = StateGraph(State)
builder.add_node("generate", generation_node)
builder.add_node("reflect", reflection_node)
builder.add_edge(START, "generate")


def should_continue(state: State):
    if len(state["messages"]) > 6:
        # End after 3 iterations
        return END
    return "reflect"


builder.add_conditional_edges("generate", should_continue)
builder.add_edge("reflect", "generate")
memory = MemorySaver()
graph = builder.compile(checkpointer=memory)

config = {"configurable": {"thread_id": "1"}}

import asyncio

async def main():
    async for event in graph.astream(
    {
        "messages": [
            HumanMessage(
                content="Generate an essay on the topicality of The Little Prince and its message in modern life"
            )
        ],
    },
    config,
):
        print(event)
        print("---")
asyncio.run(main())



#reflexion
#prob: instructions and messages all often in not well structrued text, like json
#can ai understand the format well?
#prob: how to debug a format check error?
#prob:how does the data travel from role to role ?
from langchain_core.messages import HumanMessage, ToolMessage
from langchain_core.output_parsers.openai_tools import PydanticToolsParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from pydantic import ValidationError

from pydantic import BaseModel, Field


class Reflection(BaseModel): #定义反思的数据结构，用来定义工具的参数，pydantic会自动转化为工具能懂的结构
    missing: str = Field(description="Critique of what is missing.")
    superfluous: str = Field(description="Critique of what is superfluous")

# this tool define will ask llm to generated according to the desceiption and structure given
class AnswerQuestion(BaseModel):
    """Answer the question. Provide an answer, reflection, and then follow up with search queries to improve the answer."""

    answer: str = Field(description="~25 word detailed answer to the question.")
    reflection: Reflection = Field(description="Your reflection on the initial answer.")
    search_queries: list[str] = Field(
        description="1-3 search queries for researching improvements to address the critique of your current answer."
    )


class ResponderWithRetries:
    def __init__(self, runnable, validator):
        self.runnable = runnable
        self.validator = validator

    def respond(self, state: dict):
        response = []
        for attempt in range(1):
            #print(state)
            response = self.runnable.invoke(
                {"messages": state["messages"]}, {"tags": [f"attempt:{attempt}"]}
            )
            try:
                #print(response)
                self.validator.invoke(response)# since AIGC might not fit the requirement structure, so validation is must
                return {"messages": response} # pay attention this might have many unnessasary data
            except ValidationError as e:
                state = state + [
                    response,
                    ToolMessage( # this is tool message, not ai or human 
                        content=f"{repr(e)}\n\nPay close attention to the function schema.\n\n"
                        + self.validator.schema_json()
                        + " Respond by fixing all validation errors.",
                        tool_call_id=response.tool_calls[0]["id"],
                    ),
                ]
        return {"messages": response}
    

import datetime

actor_prompt_template = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """You are expert researcher.
Current time: {time}

1. {first_instruction}
2. Reflect and critique your answer. Be severe to maximize improvement.
3. Recommend search queries to research information and improve your answer.""",
        ),
        MessagesPlaceholder(variable_name="messages"),
        (
            "user",
            "\n\n<system>Reflect on the user's original question and the"
            " actions taken thus far. Respond using the {function_name} function.</reminder>",
        ),
    ]
).partial(
    time=lambda: datetime.datetime.now().isoformat(),#把时间定为调用时间而不是代码运行的时间
)
initial_answer_chain = actor_prompt_template.partial(
    first_instruction="Provide a detailed ~25 word answer.",
    function_name=AnswerQuestion.__name__, # these two are writen internal varables, the messages are passed through args
) | llm.bind_tools(tools=[AnswerQuestion])
validator = PydanticToolsParser(tools=[AnswerQuestion])#检验工具调用后的响应是不是符合answerquestion的结构

#responder is an agent,usually has state input and output, it has ability=a chain, chain contains prompt and tool calls.
first_responder = ResponderWithRetries(
    runnable=initial_answer_chain, validator=validator
)

example_question = "Why is reflection useful in AI?"
initial = first_responder.respond(
    {"messages": [HumanMessage(content=example_question)]}
)# this is a AImessage type 






# a=initial_answer_chain.invoke({'messages':[HumanMessage(content=example_question)]})

# for k in a.additional_kwargs['tool_calls']:
#     print(k)

# print(initial['messages'][0])

revise_instructions = """Revise your previous answer using the new information.
    - You should use the previous critique to add important information to your answer.
        - You MUST include numerical citations in your revised answer to ensure it can be verified.
        - Add a "References" section to the bottom of your answer (which does not count towards the word limit). In form of:
            - [1] https://example.com
            - [2] https://example.com
    - You should use the previous critique to remove superfluous information from your answer and make SURE it is not more than 25 words.
"""


# Extend the initial answer schema to include references.
# Forcing citation in the model encourages grounded responses
class ReviseAnswer(AnswerQuestion):

    """Revise your original answer to your question. Provide an answer, reflection,

    cite your reflection with references, and finally
    add search queries to improve the answer."""

    references: list[str] = Field(
        description="Citations motivating your updated answer."
    )

#same prompt format with different tools and instruction which could have a bit varying func,
#but still, the process should be similar, the first is initial reflect, and this is reflect after

revision_chain = actor_prompt_template.partial(
    first_instruction=revise_instructions,
    function_name=ReviseAnswer.__name__,
) | llm.bind_tools(tools=[ReviseAnswer])
revision_validator = PydanticToolsParser(tools=[ReviseAnswer])

#many thing could be reused, the same agent but use different chain tool
revisor = ResponderWithRetries(runnable=revision_chain, validator=revision_validator)

import getpass
import os


def _set_if_undefined(var: str) -> None:
    # if os.environ.get(var):
    #     return
    os.environ[var] = getpass.getpass(var)

_set_if_undefined("TAVILY_API_KEY")
api_key = os.environ.get("TAVILY_API_KEY")
#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
#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
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_community.utilities.tavily_search import TavilySearchAPIWrapper
search = TavilySearchAPIWrapper()
tavily_tool = TavilySearchResults(api_wrapper=search, max_results=1)




import json

revised = revisor.respond(
    {
        "messages": [
            HumanMessage(content=example_question),
            initial["messages"],
            ToolMessage(
                tool_call_id=initial["messages"].tool_calls[0]["id"],
                content=json.dumps(
                    tavily_tool.invoke(
                        {
                            "query": initial["messages"].tool_calls[0]["args"][
                                "search_queries"
                            ][0]
                        }
                    )
                ),
            ),
        ]
    }
)
revised["messages"]



# from tavily import TavilyClient

# # Instantiate the client with your API key
# tavily_client = TavilyClient(api_key="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")

# # Perform a search query
# response = tavily_client.search(initial["messages"].tool_calls[0]["args"][
#                                 "search_queries"
#                             ][0])

# response

from langchain_core.tools import StructuredTool

from langgraph.prebuilt import ToolNode


def run_queries(search_queries: list[str], **kwargs):
    """Run the generated queries."""
    return tavily_tool.batch([{"query": query} for query in search_queries])

# why there two names of run_queries????
# how does the search_queries is attained???
tool_node = ToolNode(
    [
        StructuredTool.from_function(run_queries, name=AnswerQuestion.__name__),
        StructuredTool.from_function(run_queries, name=ReviseAnswer.__name__),
    ]
)


from typing import Literal

from langgraph.graph import END, StateGraph, START
from langgraph.graph.message import add_messages
from typing import Annotated
from typing_extensions import TypedDict


class State(TypedDict):
    messages: Annotated[list, add_messages]


MAX_ITERATIONS = 2
builder = StateGraph(State)
builder.add_node("draft", first_responder.respond)

#how is the info pass between the nodes,especially the tool nodes？？
builder.add_node("execute_tools", tool_node)
builder.add_node("revise", revisor.respond)
# draft -> execute_tools
builder.add_edge("draft", "execute_tools")
# execute_tools -> revise
builder.add_edge("execute_tools", "revise")

# Define looping logic:


def _get_num_iterations(state: list):
    i = 0
    for m in state[::-1]:
        if m.type not in {"tool", "ai"}:
            break
        i += 1
    return i


def event_loop(state: list):
    # in our case, we'll just stop after N plans
    num_iterations = _get_num_iterations(state["messages"])
    if num_iterations > MAX_ITERATIONS:
        return END
    return "execute_tools"


# revise -> execute_tools OR end
builder.add_conditional_edges("revise", event_loop, ["execute_tools", END])
builder.add_edge(START, "draft")
graph = builder.compile()





events = graph.stream(
    {"messages": [("user", "How should we handle the climate crisis?")]},
    stream_mode="values",
)
for i, step in enumerate(events):
    print(f"Step {i}")
    step["messages"][-1].pretty_print()




