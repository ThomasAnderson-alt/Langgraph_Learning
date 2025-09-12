"""
This script demonstrates how to implement loops and conditional logic using LangGraph.
It models a process that iterates a certain number of times, accumulates a result,
and then terminates based on a condition. This example showcases how to control the
flow of execution within a graph.
"""
from typing import TypedDict, Literal
from langgraph.graph import StateGraph, END



# Defines the state structure for the workflow.
class State(TypedDict):
    counter: int
    max_iterations: int
    result: int
    status: Literal["continue", "done", "error"]

# Node function: Initializes the state for the loop.
def initialize(state: State):
    print(f"Initializing counter: {state['counter']}")
    return {
        "counter": state["counter"],
        "max_iterations": state["max_iterations"],
        "result": 0,
        "status": "continue"
    }

# Node function: Performs a single iteration of the loop, updating the result.
def process_iteration(state: State):
    counter = state["counter"]
    result = state["result"]

    # Simulate the processing logic for one iteration.
    new_result = result + counter * 2

    print(f"Iteration {counter}: Current result = {new_result}")

    # Check if the loop should continue or is done.
    if counter >= state["max_iterations"]:
        status = "done"
    else:
        status = "continue"

    return {
        "counter": counter + 1,
        "max_iterations": state["max_iterations"],
        "result": new_result,
        "status": status
    }

# Node function: Handles the completion of the loop.
def handle_completion(state: State):
    print(f"Processing complete! Final result: {state['result']}")
    return state

# Node function: Handles any errors that might occur.
def handle_error(state: State):
    print("An error occurred during processing!")
    return {
        "counter": state["counter"],
        "max_iterations": state["max_iterations"],
        "result": -1,  # Use -1 as an error indicator.
        "status": "error"
    }

# Create the graph builder.
builder = StateGraph(State)

# Add the nodes to the graph.
builder.add_node("init", initialize)
builder.add_node("process", process_iteration)
builder.add_node("complete", handle_completion)
builder.add_node("error", handle_error)

# Set the entry point for the graph.
builder.set_entry_point("init")

# Add conditional edges to control the flow.
def decide_next_step(state: State):
    """Determines the next node to execute based on the status in the state."""
    if state["status"] == "error":
        return "error"
    elif state["status"] == "done":
        return "complete"
    else:
        return "process"

builder.add_conditional_edges(
    "init",
    decide_next_step,
    {
        "process": "process",
        "complete": "complete",
        "error": "error",
        "end": END
    }
)

builder.add_conditional_edges(
    "process",
    decide_next_step,
    {
        "process": "process",
        "complete": "complete",
        "error": "error",
        "end": END
    }
)


# For the 'complete' node, the workflow always ends.
builder.add_conditional_edges(
    "complete",
    lambda state: "end",
    {
        "end": END
    }
)

builder.add_conditional_edges(
    "error",
    decide_next_step,
    {
        "end": END
    }
)

# Compile the graph.
graph = builder.compile()

# Execute the graph with different test cases.
if __name__ == "__main__":
    # Define test cases with different iteration counts.
    test_cases = [
        {"counter": 1, "max_iterations": 3, "result": 0, "status": "continue"},
        {"counter": 1, "max_iterations": 5, "result": 0, "status": "continue"},
        {"counter": 1, "max_iterations": 0, "result": 0, "status": "continue"}  # An edge case to test.
    ]

    for case in test_cases:
        print("=" * 50)
        print(f"Test case: Initial counter = {case['counter']}, Max iterations = {case['max_iterations']}")

        # Explicitly cast the dictionary to the State type for clarity.
        state: State = {
            "counter": case["counter"],
            "max_iterations": case["max_iterations"],
            "result": case["result"],
            "status": case["status"]
        }
        result = graph.invoke(state)
        print(f"Final status: {result['status']}, Result: {result['result']}")



'''Output:
==================================================
Test case: Initial counter = 1, Max iterations = 3
Initializing counter: 1
Iteration 1: Current result = 2
Iteration 2: Current result = 6
Iteration 3: Current result = 12
Processing complete! Final result: 12
Final status: done, Result: 12
==================================================
Test case: Initial counter = 1, Max iterations = 5
Initializing counter: 1
Iteration 1: Current result = 2
Iteration 2: Current result = 6
Iteration 3: Current result = 12
Iteration 4: Current result = 20
Iteration 5: Current result = 30
Processing complete! Final result: 30
Final status: done, Result: 30
==================================================
Test case: Initial counter = 1, Max iterations = 0
Initializing counter: 1
Iteration 1: Current result = 2
Processing complete! Final result: 2
Final status: done, Result: 2

Summary:
This script illustrates how LangGraph can be used to create workflows with loops and
conditional branching. It defines a state with a counter and a maximum number of
iterations. The graph starts with an initialization step, then repeatedly calls a
processing node until the counter reaches the maximum. A conditional edge function
routes the flow, demonstrating how to control execution based on the current state.
This example provides a clear model for building complex, stateful applications with
controlled execution flows in LangGraph.
'''