"""
This script demonstrates how to create an AI agent with tool-calling capabilities
using LangGraph. The agent can understand user queries related to time and weather
and use external tools to fetch the requested information. This example showcases
how to integrate external functions into a stateful workflow.
"""
from typing import TypedDict, List, Annotated
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
import datetime
import requests



# Defines the state for the conversation, including messages, fetched data, and the
# current step in the workflow.
class State(TypedDict):
    messages: Annotated[List[str], add_messages]  # The history of the conversation.
    current_time: str  # The most recently fetched time.
    weather_data: str  # The most recently fetched weather information.
    step: str  # The current step: "process", "get_time", "get_weather", or "respond".

# Returns the current system time as a formatted string.
def get_current_time():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def get_weather(city: str):
    """
    Fetches the current weather for a given city using the OpenWeatherMap API.
    Returns a string with the weather description and temperature, or an error message.
    """
    API_KEY = "76db90bb7f7a32b11b2e480dcee92b8c"
    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
        weather = data['weather'][0]['description'].capitalize()
        temp = data['main']['temp']
        return f"{weather}, {temp}°C"
    except Exception as e:
        return f"Failed to fetch weather: {e}"

def process_input(state: State):
    """
    Determines the user's intent from their message and sets the next step in the
    state machine.
    """
    user_message = state["messages"][-1] if state["messages"] else ""
    if not isinstance(user_message, str):
        user_message = getattr(user_message, 'content', str(user_message))
    if "time" in user_message.lower():
        next_step = "get_time"
    elif "weather" in user_message.lower():
        next_step = "get_weather"
    else:
        next_step = "respond"
    return {
        "messages": state["messages"],
        "current_time": "",
        "weather_data": "",
        "step": next_step
    }

def fetch_time(state: State):
    """
    Gets the current time using the tool and updates the state.
    """
    return {
        "messages": state["messages"],
        "current_time": get_current_time(),
        "weather_data": state["weather_data"],
        "step": "respond"
    }

def fetch_weather(state: State):
    """
    Extracts the city from the user's message and fetches the weather data using
    the tool.
    """
    user_message = state["messages"][-1]
    if not isinstance(user_message, str):
        user_message = getattr(user_message, 'content', str(user_message))
    allowed_cities = ["Hong Kong", "Macau", "Taipei"]
    city = None
    for c in allowed_cities:
        if c.lower() in user_message.lower():
            city = c
            break
    if not city:
        weather_data = "Sorry, I can only provide weather information for Hong Kong, Macau, or Taipei."
    else:
        weather_data = get_weather(city)
    return {
        "messages": state["messages"],
        "current_time": state["current_time"],
        "weather_data": weather_data,
        "step": "respond"
    }

def generate_response(state: State):
    """
    Generates a response for the user based on the information gathered in the
    current state.
    """
    user_message = state["messages"][-1]
    if state["current_time"]:
        response = f"The current time is: {state['current_time']}"
    elif state["weather_data"]:
        response = f"The weather is: {state['weather_data']}"
    else:
        response = f"Hello! You said: '{user_message}'. I can help you check the time and weather information."
    return {
        "messages": [response],
        "current_time": state["current_time"],
        "weather_data": state["weather_data"],
        "step": "end"
    }

# Build the state machine graph and define the transitions.
builder = StateGraph(State)
builder.add_node("process", process_input)
builder.add_node("get_time", fetch_time)
builder.add_node("get_weather", fetch_weather)
builder.add_node("respond", generate_response)
builder.set_entry_point("process")

def decide_next_step(state: State):
    return state["step"]
builder.add_conditional_edges(
    "process",
    decide_next_step,
    {
        "get_time": "get_time",
        "get_weather": "get_weather",
        "respond": "respond",
        "end": END
    }
)
builder.add_conditional_edges(
    "get_time",
    decide_next_step,
    {"respond": "respond", "end": END}
)
builder.add_conditional_edges(
    "get_weather",
    decide_next_step,
    {"respond": "respond", "end": END}
)
builder.add_conditional_edges(
    "respond",
    decide_next_step,
    {"end": END}
)
graph = builder.compile()
if __name__ == "__main__":
    queries = [
        "Hello",
        "What time is it now?",
        "How is the weather in Hong Kong, Macau?",
        "How is the weather in Beijing?"
    ]
    for query in queries:
        print("=" * 50)
        print(f"User query: {query}")
        initial_state: State = {
            "messages": [query],
            "current_time": "",
            "weather_data": "",
            "step": "process"
        }
        result = graph.invoke(initial_state)
        print(f"AI response: {result['messages'][-1]}")


'''Output:
==================================================
User query: Hello
AI response: content="Hello! You said: 'content='Hello' additional_kwargs={} response_metadata={} id='51a4b465-3a1b-4c24-a5a9-157a6a650952''. I can help you check the time and weather information." additional_kwargs={} response_metadata={} id='fed4e4eb-7841-4b70-8e24-b7f731c2a6d4'
==================================================
User query: What time is it now?
AI response: content='The current time is: 2025-09-05 13:25:50' additional_kwargs={} response_metadata={} id='abf84933-785d-4960-9d72-cd9226efb15f'
==================================================
User query: How is the weather in Hong Kong?
AI response: content='The weather is: Overcast clouds, 31.75°C' additional_kwargs={} response_metadata={} id='5415f859-6c6e-440f-ab53-a1f409cc331f'
==================================================
User query: How is the weather in Beijing?
AI response: content='The weather is: Sorry, I can only provide weather information for Hong Kong, Macau, or Taipei.' additional_kwargs={} response_metadata={} id='a6590e65-9f6d-416f-bcb9-80f71c8579fe'

Summary:
This script demonstrates how to build an AI agent that can use external tools to
answer user queries. The agent can determine the user's intent, call the appropriate
tool (for time or weather), and generate a response based on the tool's output.
The LangGraph state machine orchestrates this process, managing the flow of
information and control between the different steps. This example showcases a
practical application of tool-calling in a stateful, conversational AI system.
'''