# LangGraph Project

This repository contains a collection of Python scripts and documentation demonstrating the features and practical applications of the LangGraph orchestration framework. LangGraph is designed for building, managing, and deploying long-running, stateful agents and workflows. Each file in this project illustrates a specific concept or use case, with detailed explanations and runnable code.

## File Summaries

### Core Documentation
- **LangGraph_Core_Feature.md**: Comprehensive overview of LangGraph's architecture, core features, and practical usage, including stateful workflows, loops, conditions, memory, and multi-agent collaboration.

### Approval Workflow
- **Langgraph_Approval.md**: Step-by-step introduction to a multi-step workflow approval system using LangGraph, modeling business processes with conditional logic and state management.
- **Langgraph_Approval.py**: Implementation of the approval workflow, including state definitions, node functions, and workflow graph construction.

### Conversational Chatbot
- **Langgraph_Chatbot.md**: Guide to building a basic conversational chatbot using LangGraph and an LLM API, with state management and interactive loop.
- **Langgraph_Chatbot.py**: Code for a simple chatbot that manages conversation state and calls an external LLM API for responses.

### Loops and Conditional Logic
- **Langgraph_Loop_Condition.md**: Explanation of implementing loops and conditional logic in LangGraph workflows.
- **Langgraph_Loop_Condition.py**: Example of a workflow that iterates a set number of times, accumulates results, and terminates based on conditions.

### Memory and Stateful Execution
- **Langgraph_Memory.md**: Demonstrates maintaining memory and state across workflow iterations.
- **Langgraph_Memory.py**: Code for a stateful workflow that tracks and updates state through loops and conditions.

### Multi-Agent Collaboration
- **Langgraph_Multianget.md**: Introduction to orchestrating multiple agents (analyst, solver, evaluator) in a collaborative workflow.
- **Langgraph_Multianget.py**: Implementation of a multi-agent system using LangGraph, with agent functions and state transitions.

### Simple State Machine
- **Langgraph_Simple_State_Machine.md**: Overview of a basic state machine with sequential steps using LangGraph.
- **Langgraph_Simple_State_Machine.py**: Code for a simple workflow that adds and doubles a value, demonstrating state transitions.

### Tool-Calling Agent
- **Langgraph_Tool_Calling.md**: Guide to building an AI agent with tool-calling capabilities (e.g., time and weather queries).
- **Langgraph_Tool_Calling.py**: Implementation of a tool-calling agent that integrates external APIs for time and weather information.

### Miscellaneous
- **__pycache__/**: Compiled Python files for performance optimization (auto-generated).

## Getting Started
1. Clone this repository.
2. Install the required dependencies (see individual scripts for requirements).
3. Run any script with Python 3.8+ to explore LangGraph features.

## License
This project is for educational and demonstration purposes.
