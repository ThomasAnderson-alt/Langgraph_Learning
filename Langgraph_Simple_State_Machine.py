"""
This script demonstrates a simple state machine using LangGraph, showcasing basic
state transitions. It defines a workflow with two main steps: adding one to a value
and then doubling it, illustrating how to create nodes and conditional edges to
control the flow of execution.
"""
# Import required modules and types
from typing import TypedDict, Literal
from langgraph.graph import StateGraph, END



# Defines the state for the simple state machine, including the current value and
# the current step in the process.
class State(TypedDict):
    value: int                      # The current value being processed.
    step: Literal["add", "double", "end"]  # The current step in the workflow.

# Adds one to the value and transitions the state to the 'double' step.
def add_one(state: State) -> State:
    return {"value": state["value"] + 1, "step": "double"}

# Doubles the value and transitions the state to the 'end' step.
def double_value(state: State) -> State:
    return {"value": state["value"] * 2, "step": "end"}

# Build the LangGraph state machine.
builder = StateGraph(State)
builder.add_node("add_one", add_one)           # The node to add one to the value.
builder.add_node("double_value", double_value) # The node to double the value.
builder.set_entry_point("add_one")             # The entry point is the 'add_one' node.

# Add conditional transitions between the nodes based on the 'step' in the state.
builder.add_conditional_edges(
    "add_one",
    lambda state: state["step"],
    {
        "double": "double_value",
        "end": END
    }
)
builder.add_conditional_edges(
    "double_value",
    lambda state: state["step"],
    {
        "end": END
    }
)

# Compile the graph.
graph = builder.compile()

if __name__ == "__main__":
    # Define the initial state for the state machine.
    initial_state: State = {"value": 5, "step": "add"}

    # Run the graph to completion.
    result = graph.invoke(initial_state)

    print(f"Initial value: {initial_state['value']}")
    print(f"Final value: {result['value']}")
    print("Execution steps:")
    # Print each state in the execution stream to show the progression.
    for state in graph.stream(initial_state):
        print(state)



'''Output:
Initial value: 5
Final value: 12
Execution steps:
{'value': 5, 'step': 'add'}
{'value': 6, 'step': 'double'}
{'value': 12, 'step': 'end'}

Summary:
This script demonstrates a basic state machine where an initial value is first
incremented by one and then doubled. The LangGraph implementation clearly shows how
to define a state, create nodes for each processing step, and use conditional edges
to transition between states. This example serves as a fundamental illustration of
how to build simple, sequential workflows in LangGraph.
'''
