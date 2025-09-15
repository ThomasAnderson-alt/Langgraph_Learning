# LangGraph Learning Project

[![Python Version](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/downloads/release/python-3120/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Langchain](https://img.shields.io/badge/Langchain-v0.2.5-blue.svg)](https://www.langchain.com/)
[![Langgraph](https://img.shields.io/badge/Langgraph-v0.1.0-blue.svg)](https://langchain-ai.github.io/langgraph/)

This repository contains a collection of Python scripts and corresponding Markdown files that demonstrate various features and concepts of the LangGraph library. Each Python script is a self-contained example that can be run independently, and the accompanying Markdown file provides a detailed explanation of the code and the concepts it illustrates.

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Examples](#examples)
- [Contributing](#contributing)
- [License](#license)

## Introduction

LangGraph is a library for building stateful, multi-agent applications with LLMs. It extends the LangChain expression language with the ability to coordinate multiple chains (or actors) across multiple steps of computation in a cyclic manner. This project serves as a practical guide to understanding and implementing LangGraph for various use cases.

## Features

This project covers the following LangGraph features:

- **Simple State Machine**: Demonstrates the basic setup of a LangGraph state machine.
- **Chatbot**: Implements a simple chatbot using LangGraph.
- **Tool Calling**: Shows how to integrate and use tools within a LangGraph application.
- **Conditional Looping**: Illustrates how to create loops with conditional exit points.
- **Multi-agent Collaboration**: Provides an example of multiple agents working together to solve a problem.
- **State Persistence and Cycles**: Explains how to manage state and handle cycles in the graph.
- **Memory Management**: Covers how to incorporate memory into a LangGraph application.

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/ThomasAnderson-alt/Langgraph_Learning.git
   cd Langgraph_Learning
   ```

2. **Create a virtual environment:**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. **Install the required dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

   _(Note: A `requirements.txt` file is not yet present but will be added in a future update.)_

## Usage

Each example can be run directly from the command line. For instance, to run the simple state machine example:

```bash
python Langgraph_Simple_State_Machine.py
```

Each `.py` file has a corresponding `.md` file that explains the code in detail. It is recommended to read the Markdown file before or alongside studying the Python script.

## Examples

Here is a brief overview of the examples included in this project:

- **`Langgraph_Simple_State_Machine.py`**: A basic example of creating a graph and defining nodes and edges.
- **`Langgraph_Chatbot.py`**: A simple chatbot that uses a graph to manage the conversation flow.
- **`Langgraph_Tool_Calling.py`**: Demonstrates how to define and use tools within the graph.
- **`Langgraph_Loop_Condition.py`**: An example of a graph that continues to execute a node until a certain condition is met.
- **`Langgraph_Multianget.py`**: A more complex example showcasing a multi-agent setup with a supervisor.
- **`Langgraph_Memory.py`**: Shows how to add memory to the graph to maintain conversation history.
- **`Langgraph_Approval.py`**: An example of a graph that requires human-in-the-loop approval to proceed.

## Contributing

Contributions are welcome! If you have an idea for a new example or an improvement to an existing one, please feel free to open an issue or submit a pull request.

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.
