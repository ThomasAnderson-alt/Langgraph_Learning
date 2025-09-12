"""
This script demonstrates a multi-agent collaboration scenario using LangGraph, where
different AI agents (analyst, solver, and evaluator) work together to solve a
problem. It showcases how to define a state machine that orchestrates the
interaction between these agents, allowing them to pass information and control
the flow of execution.
"""
# Import required modules and types
from typing import TypedDict, List, Annotated, cast
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages



# Defines the state for the multi-agent workflow, including the conversation history,
# problem, solution, evaluation, and the current step.
class State(TypedDict):
    messages: Annotated[List[str], add_messages]  # A list of messages exchanged between agents.
    problem: str                                 # The problem to be solved.
    solution: str                                # The current proposed solution.
    evaluation: str                              # The evaluation of the solution.
    step: str                                    # The current step in the workflow: "analyze", "solve", "evaluate", or "refine".

def analyst_agent(state: State):
    """
    The analyst agent analyzes the problem and prepares it for the solver.
    """
    problem = state["messages"][-1] if state["messages"] else state["problem"]
    analysis = f"[Analyst] Problem Analysis: The user needs to solve a math problem. The problem is: {problem}"
    return {
        "messages": state["messages"] + [analysis],
        "problem": problem,
        "solution": "",
        "evaluation": "",
        "step": "solve"
    }

def solver_agent(state: State):
    """
    The solver agent attempts to solve the problem based on the analysis.
    """
    problem = state["problem"]

    # A simple logic to solve basic arithmetic problems.
    if "+" in problem:
        parts = problem.split("+")
        a, b = int(parts[0]), int(parts[1])
        solution = f"{a} + {b} = {a + b}"
    elif "-" in problem:
        parts = problem.split("-")
        a, b = int(parts[0]), int(parts[1])
        solution = f"{a} - {b} = {a - b}"
    else:
        solution = "Unable to solve this problem."

    return {
        "messages": state["messages"] + [f"[Solver] Solution: {solution}"],
        "problem": state["problem"],
        "solution": solution,
        "evaluation": "",
        "step": "evaluate"
    }

def evaluator_agent(state: State):
    """
    The evaluator agent assesses the solution and determines the next step.
    """
    solution = state["solution"]

    # Evaluate the proposed solution.
    if "Unable" in solution:
        evaluation = "The solution was unsuccessful. The problem needs to be re-analyzed."
        next_step = "analyze"
    else:
        evaluation = "The solution is valid and can be provided to the user."
        next_step = "end"

    return {
        "messages": state["messages"] + [f"[Evaluator] Evaluation Result: {evaluation}"],
        "problem": state["problem"],
        "solution": state["solution"],
        "evaluation": evaluation,
        "step": next_step
    }

# Build the LangGraph state machine for the multi-agent collaboration.
builder = StateGraph(State)
builder.add_node("analyze", analyst_agent)      # The analyst node.
builder.add_node("solve", solver_agent)         # The solver node.
builder.add_node("evaluate", evaluator_agent)   # The evaluator node.
builder.set_entry_point("analyze")              # The entry point is the analyst.

# Determines the next step based on the current state.
def decide_next_step(state: State):
    return state["step"]

# Add conditional transitions between the nodes based on the workflow logic.
builder.add_conditional_edges("analyze", decide_next_step, {"solve": "solve", "end": END})
builder.add_conditional_edges("solve", decide_next_step, {"evaluate": "evaluate", "end": END})
builder.add_conditional_edges("evaluate", decide_next_step, {"analyze": "analyze", "end": END})

# Compile the graph.
graph = builder.compile()

if __name__ == "__main__":
    # A list of problems to be processed by the agents.
    problems = ["100 + 250", "300-123", " 42 + 58 ", "999 - 1"]

    for problem in problems:
        print("=" * 50)
        print(f"Processing problem: {problem}")

        # Initialize the state for each problem.
        initial_state = {
            "messages": [],
            "problem": problem,
            "solution": "",
            "evaluation": "",
            "step": "analyze"
        }

        # Stream the execution process and print each state, with a stop condition to prevent infinite loops.
        max_steps = 20
        last_state = None
        hit_limit = False
        for i, state in enumerate(graph.stream(cast(State, initial_state))):
            print(f"State: {state}")
            last_state = state
            if i + 1 >= max_steps:
                print(f"[Warning] Maximum step count ({max_steps}) reached. Stopping execution to prevent infinite loop.")
                hit_limit = True
                break

        # If the step limit was hit, use the last state; otherwise, invoke the graph to completion.
        if hit_limit:
            final_state = last_state
            print("[Warning] The graph did not reach an end state due to step limit.")
        else:
            final_state = graph.invoke(cast(State, initial_state))

        # Print the final result and the full conversation history.
        if final_state is not None:
            print(f"Final result: {final_state.get('solution', '')}")
            print("Conversation history:")
            for msg in final_state.get("messages", []):
                print(msg)
        else:
            print("No final state was produced.")



'''Output:
Final result: 100 + 250 = 350
Conversation history:
[Analyst] Problem Analysis: The user needs to solve a math problem. The problem is: 100 + 250
[Solver] Solution: 100 + 250 = 350
[Evaluator] Evaluation Result: The solution is valid and can be provided to the user.
Final result: 300 - 123 = 177
Conversation history:
[Analyst] Problem Analysis: The user needs to solve a math problem. The problem is: 300-123
[Solver] Solution: 300 - 123 = 177
[Evaluator] Evaluation Result: The solution is valid and can be provided to the user.
Final result: 42 + 58 = 100
Conversation history:
[Analyst] Problem Analysis: The user needs to solve a math problem. The problem is:  42 + 58
[Solver] Solution: 42 + 58 = 100
[Evaluator] Evaluation Result: The solution is valid and can be provided to the user.
Final result: 999 - 1 = 998
Conversation history:
[Analyst] Problem Analysis: The user needs to solve a math problem. The problem is
[Evaluator] Evaluation Result: The solution is valid and can be provided to the user.

Summary:
This script demonstrates a multi-agent workflow where different agents collaborate to
solve a problem. An analyst agent first analyzes the problem, a solver agent proposes
a solution, and an evaluator agent assesses the solution's validity. The LangGraph
state machine orchestrates this process, using conditional edges to transition
between agents based on the current state. This example showcases how to build
complex, collaborative systems with multiple AI agents using LangGraph.
'''