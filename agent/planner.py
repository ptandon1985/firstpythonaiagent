# library that allows Python code to communicate with Ollama Models - pip intall openai
import asyncio

from openai import OpenAI
# library that allows Python code to read configuration from .env file - pip install python-dotenv
from dotenv import load_dotenv
# library is python os package that allows Python code to read environment variables
import os

# load configuration from .env file
load_dotenv()

# Create Chat client that communicates with Ollama API
client = OpenAI(
    base_url=os.getenv("BASE_URL"),
    api_key=os.getenv("API_KEY")
)

def build_tool_description(tools):
    descriptions = ""
    for tool in tools:
        descriptions += f"Tool Name: {tool.name}\n"
        descriptions += f"Description: {tool.description}\n"

    #print("Tool Descriptions:", descriptions)
    return descriptions

def planner(state, tools):
    tool_descriptions = build_tool_description(tools)
    prompt = f"""
You are an AI Planner.
Available Tools: {tool_descriptions}
User Request: {state["user_request"]}
Completed Actions: {state["actions"]}
Previous Observation: {state["observations"]}
Instructions: 
1. Choose only ONE next action
2. Never repeat an action which is completed
3. Use observation to decide what is still required
4. If user request is completely satisfied, return FINISH
5. Return only tool name or FINISH
6. Do not explain your answer
Next Action:
"""
    response = client.chat.completions.create(
        model=os.getenv("MODEL"),   
        messages=[{"role": "system", "content": "You are a AI Planner"},
                  {"role": "user", "content": prompt}
                ]
    )
    selected_tool = response.choices[0].message.content.strip()
    return selected_tool    
