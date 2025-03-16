
import os

from mem0 import MemoryClient

from typing import Sequence
from autogen_core import CancellationToken
from autogen_agentchat.agents import BaseChatAgent
from autogen_agentchat.messages import TextMessage, ChatMessage
from autogen_agentchat.base import Response

# class CustomAgent(BaseChatAgent):
#     async def on_messages(self, messages: Sequence[ChatMessage], cancellation_token: CancellationToken) -> Response:
#         return Response(chat_message=TextMessage(content="Custom reply", source=self.name))

#     async def on_reset(self, cancellation_token: CancellationToken) -> None:
#         pass

#     @property
#     def produced_message_types(self) -> Sequence[type[ChatMessage]]:
#         return (TextMessage,)
    

os.environ["OPENAI_API_KEY"] = "sk-dba351629c004c41b3c4c99c9e806db4"
os.environ["MEM0_API_KEY"] = "m0-Fc8IYnpx8V9bisJqa44bKSV6cnf64JyAhU1CLsfO"

#from mem0 import MemoryClient
#client = MemoryClient(api_key="m0-Fc8IYnpx8V9bisJqa44bKSV6cnf64JyAhU1CLsfO")

from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.ui import Console
from autogen_ext.models.openai import OpenAIChatCompletionClient


# # Define a tool
# async def get_weather(city: str) -> str:
#     return f"The weather in {city} is 73 degrees and Sunny."

# from autogen_ext.models.openai._model_info import ModelInfo



# async def main() -> None:
#     # Define an agent
#     chat_agent = AssistantAgent(
#         name="chat_agent",
#         model_client=OpenAIChatCompletionClient(
#             model="deepseek-chat",
#             base_url="https://api.deepseek.com",
#             api_key=os.environ.get("OPENAI_API_KEY"),
           
#         ),
#        # tools=[get_weather],
#     )

#     # Define a team with a single agent and maximum auto-gen turns of 1.
#     agent_team = RoundRobinGroupChat([chat_agent], max_turns=1)

#     while True:
#         # Get user input from the console.
#         #user_input = input("Enter a message (type 'exit' to leave): ")
#         user_input ="how are you doing?"
#         #if user_input.strip().lower() == "exit":
#         #    break
#         # Run the team and stream messages to the console.
#         stream = agent_team.run_stream(task=user_input)
#         await Console(stream)

# if __name__ == "__main__":
#     import asyncio
#     asyncio.run(main())


# from autogen_agentchat import Agent, Message, MessageContext, default_subscription, message_handler, SingleThreadedAgentRuntime
# import httpx  # We'll use httpx for HTTP requests

# # Create DeepSeek Agent
# @default_subscription
# class DeepSeekAgent(Agent):
#     def __init__(self):
#         super().__init__("DeepSeek Agent")
#         self.api_key = os.environ.get("OPENAI_API_KEY")  # Using the same API key from environment
#         self.base_url = "https://api.deepseek.com/v1"

#     @message_handler
#     async def handle_message(self, message: Message, ctx: MessageContext) -> None:
#         # Generate response using DeepSeek model
#         response = self.deepseek_client.generate_response(message.content)
        
#         # Print the response (for debugging)
#         print(f"DeepSeek Agent Response: {response}")
        
#         # Send the response back
#         await self.publish_message(Message(content=response), ctx.topic_id)

# # Register Agents
# async def register_agents():
#     deepseek_agent = DeepSeekAgent(deepseek_client)
#     await deepseek_agent.register(runtime, "deepseek_agent")

# # Set Up Runtime
# runtime = SingleThreadedAgentRuntime()

# async def main():
#     await register_agents()
#     runtime.start()
    
#     # Send an initial message to the DeepSeek agent
#     await runtime.send_message(Message(content="Hello, DeepSeek!"), "deepseek_agent")

# async def run_main():
#     await main()
#     await runtime.stop_when_idle()

# # Run the program
# import asyncio
# asyncio.run(run_main())

# Please install OpenAI SDK first: `pip3 install openai`

memory = MemoryClient()
conversation = [
    {
        "role": "assistant",
        "content": "Hi, I'm Best Buy's chatbot!\n\nThanks for being a My Best Buy TotalTM member.\n\nWhat can I help you with?",
    },
    {
        "role": "user",
        "content": 'Seeing horizontal lines on our tv. TV model: Sony - 77" Class BRAVIA XR A80K OLED 4K UHD Smart Google TV',
    },
    {
        "role": "assistant",
        "content": "Thanks for being a My Best Buy Total™ member. I can connect you to an expert immediately - just one perk of your membership!\n\nSelect the button below when you're ready to chat.",
    },
    {
        "role": "assistant",
        "content": "Good evening, thank you for choosing Best Buy, Fnu. My name is Lovely. I hope you are doing well. I'm sorry to hear that you're seeing horizontal lines on your TV.\n\nI'm absolutely committed to exploring all possible ways to assist you to fix this issue.\n\nTo ensure that we are on the right account, may I please have your email address registered with your Best Buy account?",
    },
    {"role": "user", "content": "dd@gmail.com"},
    {
        "role": "assistant",
        "content": "Perfect! Thank you for providing all the details, surely you have made my job easier by doing this. I really appreciate it.\n\nI also want to take a moment to express our heartfelt appreciation for your trust and loyalty. Thank you for being an amazing customer of BestBuy Total.\n\nCould you please help me with the order number or product's details to check it quickly?\n\nSamsung - 49\" Odyssey OLED G9 (G95SC) DQHD 240Hz 0.03ms G-Sync Compatible Curved Smart Gaming Monitor - Silver - just to confirm this is the item, right?",
    },
    {"role": "user", "content": "Order number: 112217629"},
    {
        "role": "assistant",
        "content": "Superb! Thank you for confirmation.\n\nThank you for your patience. After exploring all possible solutions, I can help you to arrange a home repair appointment for your device. Our Geek Squad experts will visit your home to inspect and fix your device.\n\nIt's great that you have a protection plan - rest assured, we've got your back! As a valued Total member, you can avail this service at a minimal service fee. This fee, applicable to all repairs, covers the cost of diagnosing the issue and any small parts needed for the repair. It's part of our 24-month free protection plan.\n\nPlease click here to review the service fee and plan coverage details -\n\nhttps://www.bestbuy.com/site/best-buy-membership/best-buy-protection/pcmcat1608643232014.c?id=pcmcat1608643232014#jl-servicefees\n\nFnu - just to confirm shall I proceed to schedule the appointment?",
    },
    {"role": "user", "content": "Yes please"},
    {"role": "assistant", "content": "When should I schedule the appointment?"},
    {"role": "user", "content": "Schedule it for tomorrow please"},
]

memory.add(messages=conversation, user_id="customer_service_bot")




from openai import OpenAI

client = OpenAI(api_key="sk-dba351629c004c41b3c4c99c9e806db4", base_url="https://api.deepseek.com")


data = "I forgot the order numnber, can you quickly tell me?"

relevant_memories = memory.search(data, user_id="customer_service_bot")
flatten_relevant_memories = "\n".join([m["memory"] for m in relevant_memories])

prompt = f"""Answer the user question considering the memories. Keep answers clear and concise.
Memories:
{flatten_relevant_memories}
\n\n
Question: {data}
"""



response = client.chat.completions.create(
    model="deepseek-chat",
    messages=[
        {"role": "system", "content": "You are a helpful assistant"},
        {"role": "user", "content": prompt},
    ],
    stream=False
)

print(response.choices[0].message.content)