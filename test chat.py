from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.ui import Console
from autogen_ext.models.openai import OpenAIChatCompletionClient

from openai import OpenAI
# client = OpenAI(
#     base_url='https://xiaoai.plus/v1',
#     # sk-xxx替换为自己的key
#     api_key='sk-IZztBsF9tDeZMf0jUrJyzsqC4Fi4olJuTXNubGFdd8Fxh7Sq'
# )


# completion = client.chat.completions.create(
#     model="gpt-3.5-turbo",
#     messages=[
#     {"role": "system", "content": "You will be given a question and many documents. You are an assistant that give judegement to decide whether the given document contains answer information  related the given questions . You should strictly reply in this format : ***** answer: yes or no ***** "  },
#     {"role": "user", "content": f"Given the Question:***  *** , given the  document:*** this is piece of information of professor *** "}
#     ]
# )
# result = completion.choices[0].message.content
# print(result)
#from autogen_ext.models.openai import _model_info

# # Add DeepSeek model info (example parameters - check actual specs)
# _model_info.add_model_info(
#     "deepseek-chat",
#     context_length=32768,
#     max_tokens=4096,
#     is_chat_model=True
# )

# # If using a custom endpoint
# client = OpenAIChatCompletionClient(
#     model="deepseek-chat",
#     api_key="sk-dba351629c004c41b3c4c99c9e806db4",
#     base_url="https://api.deepseek.com"  # Example URL
# )


# client = OpenAI(
#     base_url='https://api.deepseek.com',
#     # sk-xxx替换为自己的key
#     api_key='sk-dba351629c004c41b3c4c99c9e806db4'
# )

# Define a tool
async def get_weather(city: str) -> str:
    return f"The weather in {city} is 73 degrees and Sunny."

async def main() -> None:
    # Define an agent
    weather_agent = AssistantAgent(
        name="weather_agent",
        model_client=OpenAIChatCompletionClient(
        model="deepseek-chat",
        api_key="sk-dba351629c004c41b3c4c99c9e806db4",
        # For DeepSeek's API endpoint
        base_url="https://api.deepseek.com/v1",
        # Force client to accept unknown model
        _skip_model_check=True  # Might vary by library version
        ),
        # model_client=client,
        tools=[get_weather],
    )

    # Define a team with a single agent and maximum auto-gen turns of 1.
    agent_team = RoundRobinGroupChat([weather_agent], max_turns=1)

    while True:
        # Get user input from the console.
        user_input = input("Enter a message (type 'exit' to leave): ")
        if user_input.strip().lower() == "exit":
            break
        # Run the team and stream messages to the console.
        stream = agent_team.run_stream(task=user_input)
        await Console(stream)


# NOTE: if running this inside a Python script you'll need to use asyncio.run(main()).
import asyncio
asyncio.run(main())