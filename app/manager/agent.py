from google.adk.agents import Agent
from google.adk.tools.agent_tool import AgentTool

# Import your agents and tools
from .sub_agents.caldendar_agent.agent import caldendar_agent
from .sub_agents.search_agent.agent import search_agent
from .tools.tools import get_current_time

root_agent = Agent(
    name="manager",
    # Using a standard, recommended model
    model="gemini-2.0-flash-exp",
    description="A manager agent that delegates tasks to other agents and tools.",
    instruction="""
    You are a manager agent responsible for overseeing the work of other agents.
    Your job is to understand the user's request and delegate the task to the appropriate agent or tool.

    You have access to the following agents as tools:
    - **caldendar_agent**: Use for any tasks related to creating, finding, or managing calendar events.
    - **search_agent**: Use for general web searches or to find up-to-date information.

    You also have access to this function tool:
    - **get_current_time**: Use to get the current date and time.
    """,
    # All sub-agents and functions are provided in the 'tools' list
    sub_agents=[
    ],
    tools=[
        AgentTool(caldendar_agent),
        AgentTool(search_agent),
        get_current_time,
    ],
)

# from google.adk.agents import Agent
# from google.adk.tools.agent_tool import AgentTool

# from .sub_agents.caldendar_agent.agent import caldendar_agent
# from .sub_agents.search_agent.agent import search_agent
# from .tools.tools import get_current_time

# root_agent = Agent(
#     name="manager",
#     model="gemini-2.0-flash-exp",
#     description="A manager agent that delegates tasks to other agents and tools.",
#     instruction="""
#     You are a manager agent that is responsible for overseeing the work of the other agents.

#     Always delegate the task to the appropriate agent. Use your best judgement 
#     to determine which agent to delegate to.

#     You are responsible for delegating tasks to the following agent:
#     - **caldendar_agent**: Use for any tasks related to creating, finding, or managing calendar events.

#     You have access to the following agents as tools:
#     - **search_agent**: Use for general web searches or to find up-to-date information.

#     You also have access to the following tools:
#     - get_current_time
#     """,
#     sub_agents=[caldendar_agent],
#     tools=[
#         AgentTool(search_agent),
#         get_current_time,
#     ],
# )

