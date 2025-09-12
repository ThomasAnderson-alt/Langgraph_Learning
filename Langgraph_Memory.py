"""
This script demonstrates how to use LangGraph to create a stateful workflow that
maintains memory of its execution through loops and conditional logic. It models a
process that iterates a fixed number of times, accumulates a result, and terminates
based on a condition, showcasing how to manage and update state over time.
"""
from typing import TypedDict, Literal, cast
from langgraph.graph import StateGraph, END



# Defines the state structure for the workflow, including a counter, iteration limit,
# result, and status.
class State(TypedDict):
    counter: int
    max_iterations: int
    result: int
    status: Literal["continue", "done", "error"]

# Node function: Initializes the state at the beginning of the workflow.
def initialize(state: State):
    print(f"Initializing counter: {state['counter']}")
    return {
        "counter": state["counter"],
        "max_iterations": state["max_iterations"],
        "result": 0,
        "status": "continue"
    }

# Node function: Processes a single iteration of the loop, updating the result.
def process_iteration(state: State):
    counter = state["counter"]
    result = state["result"]

    # Simulate the processing logic for one iteration.
    new_result = result + counter * 2

    print(f"Iteration {counter}: Current result = {new_result}")

    # Determine if the loop should continue or is done.
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

# Node function: Handles the completion of the workflow.
def handle_completion(state: State):
    print(f"Processing complete! Final result: {state['result']}")
    return state

# Node function: Handles any errors that may occur during execution.
def handle_error(state: State):
    print("An error occurred during processing!")
    return {
        "counter": state["counter"],
        "max_iterations": state["max_iterations"],
        "result": -1,  # Use -1 to indicate an error.
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

# Add conditional edges to control the flow of execution.
def decide_next_step(state: State):
    """Determines the next node to execute based on the current status."""
    if state["status"] == "error":
        return "error"
    elif state["status"] == "done":
        return "end"
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

builder.add_conditional_edges(
    "complete",
    decide_next_step,
    {
        "end": END
    }
)

# Main execution block.
if __name__ == "__main__":
    # Compile the graph from the builder.
    graph = builder.compile()
    # Define test cases with different iteration counts.
    test_cases = [
        {"counter": 1, "max_iterations": 3, "result": 0, "status": "continue"},
        {"counter": 1, "max_iterations": 5, "result": 0, "status": "continue"},
        {"counter": 1, "max_iterations": 0, "result": 0, "status": "continue"}  # An edge case.
    ]

    for case in test_cases:
        print("=" * 50)
        print(f"Test case: Initial counter = {case['counter']}, Max iterations = {case['max_iterations']}" )
        result = graph.invoke(cast(State, case))
        print(f"Final status: {result['status']}, Result: {result['result']}")


'''Output:
==================================================
Test case: Initial counter = 1, Max iterations = 3
Initializing counter: 1
Iteration 1: Current result = 2
Iteration 2: Current result = 6
Iteration 3: Current result = 12
Final status: done, Result: 12
==================================================
Test case: Initial counter = 1, Max iterations = 5
Initializing counter: 1
Iteration 1: Current result = 2
Iteration 2: Current result = 6
Iteration 3: Current result = 12
Iteration 4: Current result = 20
Iteration 5: Current result = 30
Final status: done, Result: 30
==================================================
Test case: Initial counter = 1, Max iterations = 0
Initializing counter: 1
Iteration 1: Current result = 2
Final status: done, Result: 2

Summary:
This script demonstrates how LangGraph can be used to create a stateful, iterative
workflow that maintains memory of its state. It defines a state machine with nodes for
initialization, processing, completion, and error handling. The graph uses conditional
transitions to control the flow, repeatedly executing a processing step until a
termination condition is met. This example showcases how to build applications with
complex logic and state management in LangGraph.
'''