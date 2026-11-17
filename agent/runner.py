# library that allows Python code to communicate with Ollama Models - pip intall openai
import asyncio
from openai import OpenAI
# library that allows Python code to read configuration from .env file - pip install python-dotenv
from dotenv import load_dotenv
# library is python os package that allows Python code to read environment variables
import os
from planner import planner
from executor import execute_action
from loop import run_agent_loop
from mcp_client import *
# load configuration from .env file
load_dotenv()

# Create Chat client that communicates with Ollama API
client = OpenAI(
    base_url=os.getenv("BASE_URL"),
    api_key=os.getenv("API_KEY")
)

def format_answer(state):
    prompt = f"""
The user asked:
{state["user_request"]}
Action Performed:
{state["actions"]}
Observations:
{state["observations"]}

Answer user naturally.
Do not mention internal planning.
Do not mention state.
Do not mention tools.
"""
    response = client.chat.completions.create(
            model=os.getenv("MODEL"),   
            messages=[{"role": "user", "content": prompt}]
        )

    return response.choices[0].message.content.strip()

async def main():
    # Step 1: Connect to MCP Client
    client = await connect()
    # Step 2: Discover all available tools
    tools = await discover_tools(client)

    print()
    print("Available Tools")
    print("===============")
    for tool in tools:
        print(tool.name)

    # Step 3: Get User Inputs
    user_request = input("\nYou:")

    # Step 4: Run Agent Loop
    state = await run_agent_loop(user_request,planner, execute_action, format_answer, tools, client)

    print()
    print("\nFinal Answer:")
    print(state["final_answer"])

    # Step 5: Disconnect from MCP Client
    await disconnect(client)

if __name__ == "__main__":
    asyncio.run(main())