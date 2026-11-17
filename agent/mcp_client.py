from fastmcp import Client
from fastmcp.client.transports import StdioTransport


# Define the explicit transport with command and arguments
transport = StdioTransport(
    command="python",
    args=["Day08/mcp_server.py"]
)

async def connect():
    """Connects to the MCP server"""
    client = Client(transport=transport)
    await client.__aenter__()
    print("Connected to MCP server.")
    return client

async def disconnect(client):   
    """Disconnects from the MCP server"""
    await client.__aexit__(None, None, None)
    print("Disconnected from MCP server.")

async def discover_tools(client):
    """Retrieve all available tools on the MCP server"""
    tools = await client.list_tools()
    #print("Available tools on the MCP server:")
    #for tool in tools:
    #    print(f"- {tool}")    
    return tools    

async def execute_tool(client, tool_name, arguments=None):
    """Executes a specific tool on the MCP server"""
    if arguments is None:
        arguments = {}
    result = await client.call_tool(tool_name, arguments)   
    #print(f"Result from {tool_name}: {result}")
    return result

