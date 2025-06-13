from google.adk.agents import Agent
from google.adk.tools import google_search

# def get_current_time() -> dict:
#     """
#     Get the current time in the format YYYY-MM-DD HH:MM:SS
#     """
#     return {
#         "current_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
#     }

search_agent = Agent(
    name="search_agent",
    model="gemini-2.0-flash-exp",
    description="Agent to help with searching the web for information.",
    instruction="""
    You are a helpful assistant that can use the following tools:
    - google_search

    If the user asks about anything else, 
    you should delegate the task to the manager agent.
    """,
    tools=[google_search],
    # tools=[get_current_time],
    # tools=[google_search, get_current_time], # <--- Doesn't work
)