from state import *

async def run_agent_loop(user_request, planner, execute_action, format_answer, tools, client):
    # Step 1: Create Initial State
    state = create_state(user_request)

    while can_continue(state):
        # Planner Decides what to do next
        action = planner(state, tools)
        print("Selected Action:", action)

        if action == "FINISH":
            answer = format_answer(state)
            finish(state, answer)
            break

        # Execute Action
        observation = await execute_action(action, client)

        # Add Action
        add_actions(state, action)

        # Add Observation
        record_observation(state, action, observation)

        # Next Step
        next_step(state)

    return state
