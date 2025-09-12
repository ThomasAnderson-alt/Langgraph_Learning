"""
This script demonstrates how to build a basic conversational chatbot using LangGraph
and a large language model (LLM) API. It shows how to manage the conversation state,
call an external model to generate responses, and create a simple interactive loop.
"""
# Import required modules and types
from typing import TypedDict, Annotated, List, Union
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage
import requests



# Defines the state for the chatbot, which consists of a list of messages.
# The `add_messages` function ensures that new messages are appended to the list.
class State(TypedDict):
    messages: Annotated[List[Union[str, BaseMessage]], add_messages]

def call_model(state: State) -> dict:
    """
    Calls a large language model API to generate a response based on the current
    conversation state.
    """
    last_message = state["messages"][-1]
    # Extracts the prompt from the last message, handling both string and BaseMessage objects.
    if isinstance(last_message, BaseMessage):
        prompt = last_message.content
    else:
        prompt = str(last_message)

    # NOTE: Replace with your actual API key and endpoint.
    # In a production environment, it is recommended to use environment variables for security.
    api_key = "sk-lmzcznwaldljlkfyuauzbwijxlfaffkxasaeioyolscngoyi" 
    base_url = "https://api.siliconflow.cn/v1"
    model = "ByteDance-Seed/Seed-OSS-36B-Instruct"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "model": model,
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    }

    try:
        response = requests.post(f"{base_url}/chat/completions", headers=headers, json=data, timeout=30)
        response.raise_for_status()
        result = response.json()
        ai_response = result["choices"][0]["message"]["content"].strip()
    except Exception as e:
        ai_response = f"Sorry, there was an error: {e}"

    # Returns the AI's response as a new message to be added to the state.
    return {"messages": [ai_response]}

# Build the LangGraph for the chatbot.
builder = StateGraph(State)
builder.add_node("chatbot", call_model)  # The node for LLM interaction.
builder.set_entry_point("chatbot")        # The entry point of the graph is the chatbot node.
builder.add_edge("chatbot", END)          # The graph ends after one response.
graph = builder.compile()

if __name__ == "__main__":
    print("Chatbot is ready. Type 'exit' to end the conversation.")
    while True:
        user_input = input("You: ")
        if user_input.lower() == 'exit':
            break
        # Invoke the graph with the user's message.
        result = graph.invoke({"messages": [user_input]})
        # The result contains the updated state, and the last message is the AI's response.
        ai_response = result["messages"][-1]
        # Print the AI's response, handling both string and BaseMessage objects.
        if hasattr(ai_response, 'content'):
            print(f"AI: {ai_response.content}")
        else:
            print(f"AI: {ai_response}")



'''Output:
    Chatbot is ready. Type 'exit' to end the conversation.
    You: Hello, help me to translate the following into French: I am learning Python, I plan to develop AI in the furture.
    AI: J'apprends le Python, je compte développer de l'IA à l'avenir.  

    **Breakdown**:  
    - "I am learning Python" = *J'apprends le Python* (present tense of "apprendre" + "le Python" for the language).  
    - "I plan to develop AI" = *je compte développer de l'IA* ("compter" = "to plan/intend" + infinitive "développer"; "de l'IA" = "de l'intelligence artificielle" shortened to "de l'IA").  
    - "in the future" = *à l'avenir*.  

    Alternatively, "Je prévois de développer de l'IA à l'avenir" is also correct ("prévois de" = "plan to"). Both are natural in French.
    You: Thank you, exit. 
    AI: You're welcome! If you need help again later, don’t hesitate to come back. Have a great day! 😊
    
Summary:
This script showcases how to use LangGraph to create a simple, interactive chatbot.
It defines a state to maintain the conversation history and uses a single node to call
a language model API for generating responses. The script demonstrates how to build
and run the graph, creating a continuous loop for a conversation with the user. This
example serves as a foundational illustration of how LangGraph can be used to power
conversational AI applications.
'''