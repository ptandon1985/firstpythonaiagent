# First Python AI Agent (FastMCP + Ollama)

A modular, local-first autonomous AI agent built in Python using a **Plan–Execute–Observe** control loop, **FastMCP** over `StdioTransport` for tool isolation, and a local **Ollama** LLM (via the OpenAI-compatible Python SDK).

---

## Architecture & Execution Flow

```mermaid
flowchart TD
    classDef main fill:#1e293b,stroke:#38bdf8,stroke-width:2px,color:#f8fafc
    classDef state fill:#311042,stroke:#e879f9,stroke-width:2px,color:#f8fafc
    classDef loop fill:#1e1b4b,stroke:#818cf8,stroke-width:2px,color:#f8fafc
    classDef mcp fill:#064e3b,stroke:#34d399,stroke-width:2px,color:#f8fafc
    classDef llm fill:#451a03,stroke:#fbbf24,stroke-width:2px,color:#f8fafc

    Start(["Start: main.py"]):::main --> LoadEnv["Load .env: BASE_URL, API_KEY, MODEL"]:::main
    LoadEnv --> Connect["mcp_client.connect<br>StdioTransport: python Day09/agent/mcp_server.py"]:::mcp
    Connect <-->|"Spawn Subprocess"| MCPServer["Day09/agent/mcp_server.py<br>FastMCP Time Server<br>- current_time<br>- roll_dice<br>- generate_password"]:::mcp
    Connect --> Discover["mcp_client.discover_tools<br>client.list_tools"]:::mcp
    Discover --> UserIn["CLI Prompt: user_request from input"]:::main
    UserIn --> InitState["state.py: create_state<br>current_step=0, max_steps=5, finished=False"]:::state

    subgraph AgentLoop["loop.py: run_agent_loop"]
        direction TB
        InitState --> Guard{"state.py: can_continue?<br>not finished AND step < 5"}:::state
        Guard -->|"True"| Planner["planner.py: planner<br>build_tool_description + state prompt"]:::loop
        Planner <-->|"Chat Completion"| Ollama[("Ollama Local LLM")]:::llm
        Planner --> CheckAction{"action == FINISH?"}:::loop

        CheckAction -->|"No: Tool Name"| Exec["executor.py: execute_action<br>mcp_client.execute_tool"]:::loop
        Exec <-->|"Stdio call_tool"| MCPServer
        Exec --> Unwrap["Extract result.content text"]:::loop
        Unwrap --> Mutate["state.py:<br>1. add_actions<br>2. record_observation<br>3. next_step"]:::state
        Mutate --> Guard

        CheckAction -->|"Yes: FINISH"| Format["main.py: format_answer<br>Synthesize final response"]:::main
        Format <-->|"Chat Completion"| Ollama
        Format --> FinishState["state.py: finish<br>Set final_answer and finished=True"]:::state
    end

    FinishState -->|"break"| PrintOut["main.py: Print final_answer"]:::main
    Guard -->|"False: max_steps reached"| PrintOut
    PrintOut --> Disconnect["mcp_client.disconnect<br>Close MCP Subprocess"]:::mcp
    Disconnect --> End(["End"]):::main
```

---

## Project Structure

```text
firstpythonaiagent/
├── agent/
│   ├── main.py          # CLI entry point, .env loader, MCP lifecycle & answer synthesis
│   ├── loop.py          # Core async Plan–Execute–Observe loop
│   ├── planner.py       # Prompts Ollama to select the next tool or return FINISH
│   ├── executor.py      # Dispatches tool calls to MCP client & parses TextContent
│   ├── state.py         # State dictionary factory, step tracking & max_steps guard
│   └── mcp_client.py    # FastMCP StdioTransport client wrapper
|   └── mcp_server.py    # FastMCP ("Time Server") exposing @mcp.tool() endpoints
```

### Available MCP Tools (`Day09/agent/mcp_server.py`)
| Tool Name | Description |
| :--- | :--- |
| `current_time` | Returns the current local date and time (`YYYY-MM-DD HH:MM:SS`). |
| `roll_dice` | Simulates rolling a six-sided die (`1`–`6`). |
| `generate_password` | Generates a cryptographically random password (default length: `12`). |

---

## Prerequisites & Setup

1. **Install Ollama** and pull a local chat model (e.g., `llama3.2` or `qwen2.5`):
   ```bash
   ollama pull llama3.2
   ```

2. **Install Python dependencies**:
   ```bash
   pip install fastmcp openai python-dotenv
   ```

3. **Configure environment variables**:
   Create a `.env` file in the directory where you run `main.py`:
   ```env
   BASE_URL=http://localhost:11434/v1
   API_KEY=ollama
   MODEL=llama3.2
   ```

---

## Usage

Run the agent from the repository root so `StdioTransport` resolves `Day09/agent/mcp_server.py`:

```bash
python agent/main.py
```

### Example Session
```text
Connected to MCP server.

Available Tools
===============
current_time
roll
