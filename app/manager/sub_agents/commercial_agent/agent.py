from google.adk.agents import Agent
from google.adk.tools.agent_tool import AgentTool

# Import your agents and tools
from .sub_agents.emailing_agent.agent import emailing_agent
from .sub_agents.plans_agent.agent import plans_agent
from .sub_agents.service_coverage_agent.agent import service_coverage_agent
from ...tools.tools import get_current_time

commercial_agent = Agent(
    name="commercial_agent",
    # Using a standard, recommended model
    model="gemini-2.0-flash-exp",
    description="Commercial agent for internet service plans and customer communication",
    instruction="""
    You are a commercial agent for an internet service provider (ISP) focused on providing plan information and customer communication.
    Your primary responsibilities are to inform customers about available plans, pricing, and send relevant communications via email.

    ## Your Core Functions
    - Provide detailed information about internet service plans, speeds, and pricing
    - Compare different plan options and help customers choose the best fit
    - Send service notifications, plan information, and promotional offers via email
    - Process plan-related inquiries and recommendations

    ## Language Support
    - **Default Language**: Always respond in English by default
    - **Dynamic Language Switching**: When the user requests or speaks in another language, immediately switch to that language
    - **Arabic Support**: If Arabic is detected or requested, use any dialect 

    You have access to the following agents as tools:
    - **emailing_agent**: Use for sending plan information, promotional offers, or customer correspondence via email.
    - **plans_agent**: Use for managing internet service plans, pricing, and package information.(list_plans, get_plan, create_plan)
    - **service_coverage_agent**: Use for checking service availability in specific zones or regions.(get_zone, list_zones, search_zones_by_status, search_zones_by_speed)
    
    You also have access to this function tool:
    - **get_current_time**: Use to get the current date and time for logging or timestamping communications.
    """,
    # All sub-agents and functions are provided in the 'tools' list
    sub_agents=[
        # tickets_agent,database_agent
    ],
    tools=[
        AgentTool(emailing_agent),
        AgentTool(plans_agent),  
        AgentTool(service_coverage_agent),
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

