from datetime import datetime

import random
import secrets
import string
from fastmcp import FastMCP

mcp = FastMCP(
    "Time Server"
    )

@mcp.tool()
def current_time():
    """Returns Current date and time """
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

@mcp.tool()
def roll_dice():
    """Simulates rolling a six-sided dice and returns the result."""
    return random.randint(1, 6)

@mcp.tool()
def generate_password(length=12):
    """Generates a random password of specified length."""
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ""
    for _ in range(length):
        password += secrets.choice(characters)
    return password

if __name__ == "__main__":
    print("Starting MCP server..")
    mcp.run()