"""
This script demonstrates a multi-step workflow approval system using LangGraph.
It models a business process where a request requires multiple levels of approval
depending on the amount requested. The workflow handles approvals, rejections,
and requests for revision, showcasing conditional logic and state management.
"""
from typing import TypedDict, List, Literal, cast
from langgraph.graph import StateGraph, END
from enum import Enum



# Represents the possible approval statuses for a request.
class ApprovalStatus(Enum):
    PENDING = "pending"           # The request is awaiting approval.
    APPROVED = "approved"         # The request has been approved by an approver.
    REJECTED = "rejected"         # The request has been rejected by an approver.
    REVISION_NEEDED = "revision_needed"  # The request requires revision before proceeding.

# Defines the state of an approval request as it moves through the workflow.
class State(TypedDict):
    request_id: str                # A unique identifier for the request.
    requester: str                 # The name of the person who submitted the request.
    amount: float                  # The amount requested.
    description: str               # A description of the request.
    status: ApprovalStatus         # The current approval status of the request.
    approvals: List[str]           # A list of approvers who have approved the request.
    rejections: List[str]          # A list of approvers who have rejected the request.
    comments: List[str]            # Comments from the approvers.
    current_approver: str          # The next person to act on the request.
    revision_count: int            # The number of times the request has been revised.

def submit_request(state: State):
    """
    This is the initial node in the workflow. It handles the submission of a new request
    and sets its initial state.
    """
    print(f"Request submitted: {state['request_id']} by {state['requester']}")
    return {
        **state,
        "status": ApprovalStatus.PENDING,
        "current_approver": "manager_1"
    }

def manager_approval(state: State):
    """
    The manager reviews the request and determines the next step based on the
    requested amount.
    """
    approver = state["current_approver"]

    # The manager's approval logic is based on the amount.
    if state["amount"] <= 1000:
    # If the amount is within the manager's limit, they approve it directly.
        decision = ApprovalStatus.APPROVED
        message = f"{approver} approved the request."
        next_approver = "complete"
    elif state["amount"] <= 5000:
    # If the amount exceeds the manager's limit but is within the director's limit,
    # it is forwarded to the director for approval.
        decision = ApprovalStatus.PENDING
        message = f"{approver} approved, director approval required."
        next_approver = "director_1"
    else:
    # If the amount exceeds the director's limit, a revision is requested.
        decision = ApprovalStatus.REVISION_NEEDED
        message = f"{approver} suggests revising the amount."
        next_approver = "requester"

    return {
        **state,
        "status": decision,
        "approvals": state["approvals"] + [approver],
        "comments": state["comments"] + [message],
        "current_approver": next_approver
    }

def director_approval(state: State):
    """
    The director reviews requests that require a higher level of approval.
    """
    approver = state["current_approver"]

    # The director's approval logic.
    if state["amount"] <= 10000:
        decision = ApprovalStatus.APPROVED
        message = f"{approver} approved the request."
        next_approver = "complete"
    else:
        decision = ApprovalStatus.REJECTED
        message = f"{approver} rejected the request (amount too large)."
        next_approver = "end"

    return {
        **state,
        "status": decision,
        "approvals": state["approvals"] + [approver],
        "comments": state["comments"] + [message],
        "current_approver": next_approver
    }

def request_revision(state: State):
    """
    The requester must revise and resubmit the request. The request is automatically
    rejected after three failed revision attempts.
    """
    revision_count = state.get("revision_count", 0) + 1
    if revision_count >= 3:
        message = "Request auto-rejected after 3 unsuccessful revisions."
        return {
            **state,
            "comments": state["comments"] + [message],
            "status": ApprovalStatus.REJECTED,
            "current_approver": "end",
            "revision_count": revision_count
        }
    else:
        message = f"Please revise the request amount and resubmit. (Revision attempt {revision_count})"
        return {
            **state,
            "comments": state["comments"] + [message],
            "current_approver": "requester",
            "revision_count": revision_count
        }

def complete_request(state: State):
    """
    This is the final node of the workflow, marking the approval process as complete.
    """
    message = f"Request approval process completed. Final status: {state['status'].value}"
    return {
        **state,
        "comments": state["comments"] + [message],
        "current_approver": "end"
    }

# --- Build the workflow graph ---
builder = StateGraph(State)
builder.add_node("submit", submit_request)              # Initial submission node
builder.add_node("manager_approval", manager_approval)  # Manager review node
builder.add_node("director_approval", director_approval)  # Director review node
builder.add_node("request_revision", request_revision)  # Request revision node
builder.add_node("complete", complete_request)          # Completion node
builder.set_entry_point("submit")

def decide_next_step(state: State):
    """
    This function determines the next node to execute based on the current
    approver in the state.
    """
    if state["current_approver"] == "complete":
        return "complete"
    elif state["current_approver"] == "manager_1":
        return "manager_approval"
    elif state["current_approver"] == "director_1":
        return "director_approval"
    elif state["current_approver"] == "requester":
        return "request_revision"
    else:
        return "end"

# Define the conditional transitions for each node in the graph.
builder.add_conditional_edges(
    "submit",
    decide_next_step,
    {
        "manager_approval": "manager_approval",
        "director_approval": "director_approval",
        "request_revision": "request_revision",
        "complete": "complete",
        "end": END
    }
)
builder.add_conditional_edges(
    "manager_approval",
    decide_next_step,
    {
        "manager_approval": "manager_approval",
        "director_approval": "director_approval",
        "request_revision": "request_revision",
        "complete": "complete",
        "end": END
    }
)
builder.add_conditional_edges(
    "director_approval",
    decide_next_step,
    {
        "manager_approval": "manager_approval",
        "director_approval": "director_approval",
        "request_revision": "request_revision",
        "complete": "complete",
        "end": END
    }
)
builder.add_conditional_edges(
    "request_revision",
    decide_next_step,
    {
        "manager_approval": "manager_approval",
        "director_approval": "director_approval",
        "request_revision": "request_revision",
        "complete": "complete",
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

# Compile the workflow into a runnable graph.
graph = builder.compile()

# --- Example usage: run test cases through the workflow ---
if __name__ == "__main__":
    # A list of example requests with varying amounts and descriptions to test the workflow.
    test_cases = [
        {"request_id": "REQ001", "requester": "Alice", "amount": 500, "description": "Office supplies purchase"},
        {"request_id": "REQ002", "requester": "Robert", "amount": 3000, "description": "Team building activity"},
        {"request_id": "REQ003", "requester": "Jack", "amount": 8000, "description": "Training expenses"},
        {"request_id": "REQ004", "requester": "William", "amount": 15000, "description": "Equipment purchase"}
    ]

    for case in test_cases:
        print("=" * 50)
        print(f"Processing request: {case['request_id']} - Amount: {case['amount']}")

        initial_state = {
            **case,
            "status": ApprovalStatus.PENDING,
            "approvals": [],
            "rejections": [],
            "comments": [],
            "current_approver": "submit",
            "revision_count": 0
        }

        # Run the workflow for the current request with a stop condition and an increased recursion limit.
        def stop_condition(state: State):
            # The workflow stops if the process is at the end, the request is rejected,
            # or the revision limit has been reached.
            return (
                state["current_approver"] == "end" or
                state["status"] == ApprovalStatus.REJECTED or
                state.get("revision_count", 0) >= 3
            )

        result = graph.invoke(
            cast(State, initial_state),
            {"recursion_limit": 50},
            stop_condition=stop_condition
        )

        print(f"Final status: {result['status'].value}")
        print(f"Approvers: {', '.join(result['approvals'])}")
        print("Approval comments:")
        for comment in result['comments']:
            print(f"  - {comment}")



'''Output:
==================================================
Processing request: REQ001 - Amount: 500
Request submitted: REQ001 by Alice
Final status: approved
Approvers: manager_1
Approval comments:
  - manager_1 approved the request.
  - Request approval process completed. Final status: approved
==================================================
Processing request: REQ002 - Amount: 3000
Request submitted: REQ002 by Robert
Final status: approved
Approvers: manager_1, director_1
Approval comments:
  - manager_1 approved, director approval required.
  - director_1 approved the request.
  - Request approval process completed. Final status: approved
==================================================
Processing request: REQ003 - Amount: 8000
Request submitted: REQ003 by Jack
Final status: rejected
Approvers: manager_1
Approval comments:
  - manager_1 suggests revising the amount.
  - Please revise the request amount and resubmit. (Revision attempt 1)
  - Please revise the request amount and resubmit. (Revision attempt 2)
  - Request auto-rejected after 3 unsuccessful revisions.
==================================================
Processing request: REQ004 - Amount: 15000
Request submitted: REQ004 by William
Final status: rejected
Approvers: manager_1
Approval comments:
  - manager_1 suggests revising the amount.
  - Please revise the request amount and resubmit. (Revision attempt 1)
  - Please revise the request amount and resubmit. (Revision attempt 2)
  - Request auto-rejected after 3 unsuccessful revisions.
  
Summary:
This script demonstrates how LangGraph can be used to create a multi-step approval
workflow. It shows how to define a state, create nodes for each step in the process,
and use conditional edges to route the workflow based on the state. The example
showcases a business approval process where requests are routed to different
approvers based on the requested amount, and it includes logic for handling
rejections and revisions.
'''