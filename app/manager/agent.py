from google.adk.agents import Agent
from google.adk.tools.agent_tool import AgentTool

# Import your agents and tools
from .sub_agents.caldendar_agent.agent import caldendar_agent
from .sub_agents.gmail_agent.agent import gmail_agent
from .sub_agents.search_agent.agent import search_agent
from .sub_agents.database_agent.agent import database_agent
from .sub_agents.tickets_agent.agent import tickets_agent
from .sub_agents.commercial_agent.agent import commercial_agent
from .sub_agents.network_diagnostics_agent.agent import network_diagnostics_agent
from .tools.tools import get_current_time

root_agent = Agent(
    name="manager",
    # Using a standard, recommended model
    model="gemini-2.0-flash-exp",
    description="you are the internet Asistant",
    instruction="""
    You are a manager agent responsible for overseeing the work of other agents.
    Your job is to understand the user's request and delegate the task to the appropriate agents or tools.
    you orchestrates the tasks in a way that ensures the most efficient use of resources and time.
    you create the workflow and cordinate the work between the agents and tools to achieve the best results and with limiting the interaction with user only when needed .


    ## Language Support
    - **Default Language**: Always respond in English by default
    - **Dynamic Language Switching**: When the user requests or speaks in another language, immediately switch to that language while maintaining full functionality
    - **Arabic Support**: If Arabic is detected or requested, use any dialect
    - **Context Preservation**: Maintain all technical capabilities and contextual understanding regardless of language

    You have access to the following agents as tools:
    - **commercial_agent**: provide plans information, promotional offers.(you have access to a emailing_agent to send emails and communicate with customers also you have access to a plans_agent to manage internet service plans, pricing, and package information.)
    - **network_diagnostics_agent**: Use for network diagnostics and troubleshooting for resolving internet connection issues (sub_agents: **proactive_event_agent**: Use to schedule appointments with technical experts (human) when advanced technical support is needed, **emailing_agent**: Use to confirm the scheduling by sending an email to the user.).
    
    You also have access to this function tool:
    - **get_current_time**: Use to get the current date and time.
    """,
    # All sub-agents and functions are provided in the 'tools' list
    sub_agents=[
        # tickets_agent,database_agent
    ],
    tools=[
        AgentTool(network_diagnostics_agent),   
        AgentTool(commercial_agent),  
        get_current_time,
    ],
    # before_model_callback=[list_tickets,get_current_time,list_users]
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

