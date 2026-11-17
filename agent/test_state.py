from state import *

state = create_state("Generate Password and tell me time")

print("Initial State")
print(state)

add_actions(state, "generate_password")
record_observation(state, "generate_password", "Password: %^&hu^&875")
next_step(state)

print("\n Print State after 1st Iteration")
print(state)

finish(state, "Password: %^&hu^&875\nCurrent Time: 10:45 PM")
print("Final State")
print(state)
