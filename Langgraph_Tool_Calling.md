# Langgraph_Tool_Calling.py Detailed Step-by-Step Introduction

## Overview

This script demonstrates how to create an AI agent with tool-calling capabilities using LangGraph. The agent can understand user queries related to time and weather and use external tools to fetch the requested information.

## Code Breakdown

### 1. Imports and State Definition

- **Imports**: Brings in types, LangGraph, and utility libraries for time and HTTP requests.
- **State (TypedDict)**: Maintains conversation history, fetched data, and the current step.

### 2. Tool Functions

- **get_current_time**: Returns the current system time as a formatted string.
- **get_weather**: Fetches weather data for a city using the OpenWeatherMap API.

### 3. Node Functions

- **process_input**: Determines user intent and sets the next step.
- **fetch_time**: Gets the current time and updates the state.
- **fetch_weather**: Extracts the city from the user's message and fetches weather data.
- **generate_response**: Generates a response for the user based on the gathered information.

### 4. Graph Construction

- **StateGraph**: Nodes are added for each step. The entry point is set to `process`.
- **decide_next_step**: Determines the next node based on the current step in the state.
- **Conditional Edges**: Control the flow between nodes based on the state.
- **Compile**: The workflow is compiled into a runnable graph.

### 5. Example Usage

- **Queries**: Several user queries are processed, demonstrating tool-calling and response generation.

## How the Code Achieves Its Goal

- **Tool Integration**: Integrates external tools for time and weather information.
- **Intent Recognition**: Uses state and conditional logic to determine user intent and route the workflow.
- **Traceability**: Prints each step and response for transparency.

## Summary

This script is a practical example of using LangGraph to build an AI agent with tool-calling capabilities, suitable for conversational AI systems.
