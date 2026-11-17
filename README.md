flowchart TD
    %% Styling
    classDef main fill:#1e293b,stroke:#38bdf8,stroke-width:2px,color:#f8fafc
    classDef state fill:#311042,stroke:#e879f9,stroke-width:2px,color:#f8fafc
    classDef loop fill:#1e1b4b,stroke:#818cf8,stroke-width:2px,color:#f8fafc
    classDef mcp fill:#064e3b,stroke:#34d399,stroke-width:2px,color:#f8fafc
    classDef llm fill:#451a03,stroke:#fbbf24,stroke-width:2px,color:#f8fafc

    Start([Start: main.py]):::main --> LoadEnv[Load .env: BASE_URL, API_KEY, MODEL]:::main
    LoadEnv --> Connect[mcp_client.connect<br/>StdioTransport: python Day08/mcp_server.py]:::mcp
    Connect <-->|Spawn Subprocess| MCPServer[Day08/mcp_server.py<br/>FastMCP 'Time Server'<br/>• current_time<br/>• roll_dice<br/>• generate_password]:::mcp
    Connect --> Discover[mcp_client.discover_tools<br/>client.list_tools]:::mcp
    Discover --> UserIn[/CLI Prompt: user_request = input 'You:'/]:::main
    UserIn --> InitState[state.py: create_state<br/>current_step=0, max_steps=5, finished=False]:::state

    subgraph AgentLoop ["loop.py: run_agent_loop()"]
        direction TB
        InitState --> Guard{state.py: can_continue?<br/>not finished AND step < 5}:::state
        Guard -->|True| Planner[planner.py: planner<br/>build_tool_description + state prompt]:::loop
        Planner <-->|Chat Completion| Ollama[(Ollama Local LLM)]:::llm
        Planner --> CheckAction{action == 'FINISH'?}:::loop

        CheckAction -->|No: Tool Name| Exec[executor.py: execute_action<br/>mcp_client.execute_tool]:::loop
        Exec <-->|Stdio call_tool| MCPServer
        Exec --> Unwrap[Extract result.content&#91;0&#93;.text]:::loop
        Unwrap --> Mutate[state.py:<br/>1. add_actions<br/>2. record_observation<br/>3. next_step step += 1]:::state
        Mutate --> Guard

        CheckAction -->|Yes: FINISH| Format[main.py: format_answer<br/>Synthesize without leaking internals]:::main
        Format <-->|Chat Completion| Ollama
        Format --> FinishState[state.py: finish<br/>final_answer = answer, finished = True]:::state
    end

    FinishState -->|break| PrintOut[/main.py: Print state&#91;'final_answer'&#93;/]:::main
    Guard -->|False: max_steps reached| PrintOut
    PrintOut --> Disconnect[mcp_client.disconnect<br/>client.__aexit__]:::mcp
    Disconnect --> End([End]):::main
