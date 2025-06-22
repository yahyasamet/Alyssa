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
from .sub_agents.case_summary_agent.agent import case_summary_agent
from .tools.tools import get_current_time

root_agent = Agent(
    name="manager",
    # Using a standard, recommended model
    model="gemini-2.0-flash-exp",
    description="you are the internet Asistant",
    instruction="""
    You are a manager agent responsible for overseeing the work of other agents.
    Your job is to understand the user's request as an internet provider customer support and delegate the task to the appropriate agents or tools.
    you orchestrates the tasks in a way that ensures the most efficient use of resources and time.
    you create the workflow and cordinate the work between the agents and tools to achieve the best results and with limiting the interaction with user only when needed .

    ## Client Context
    - **Client ID Handling**: When a client ID is provided, use it to personalize the service and retrieve relevant customer information
    - **Customer Identification**: Always reference the client ID when accessing customer data, service history, or account information
    - **Personalization**: Use the client ID to provide tailored support based on the customer's service plan, history, and preferences
    - **Data Privacy**: Only access and share information relevant to the provided client ID
    - **No Client ID**: If no client ID is provided, offer general support and request identification when needed for account-specific tasks

    ## Language Support
    - **Default Language**: Always respond in English by default
    - **Dynamic Language Switching**: When the user requests or speaks in another language, immediately switch to that language while maintaining full functionality
    - **Arabic Support**: If Arabic is detected or requested, use any dialect
    - **Context Preservation**: Maintain all technical capabilities and contextual understanding regardless of language

    You have access to the following agents as tools:
    - **commercial_agent**: provide plans information, promotional offers.(you have access to a emailing_agent to send emails and communicate with customers also you have access to a plans_agent to manage internet service plans, pricing, and package information.)
    - **network_diagnostics_agent**: Use for network diagnostics and troubleshooting for resolving internet connection issues (sub_agents: **proactive_event_agent**: Use to schedule appointments with technical experts (human) when advanced technical support is needed, **emailing_agent**: Use to confirm the scheduling by sending an email to the user. **invoice_agent**: Use to check if the customer has any outstanding invoices that might affect their service.).
    - **database_agent**: Use for database management tasks, such as retrieving or updating user information and handling new subscriptions. Always use the client ID when provided to ensure accurate data retrieval.
    Before calling any agent make sure to use the **case_summary_agent** to summarize the conversation and provide a clear context for the task at hand.
    You also have access to this function tool:
    - **get_current_time**: Use to get the current date and time.

    ## Client ID Usage Guidelines:
    1. When a client ID is provided, immediately acknowledge it and use it for all subsequent operations
    2. Pass the client ID to relevant agents (especially database_agent) for customer-specific operations
    3. If client ID is missing for account-specific requests, politely ask for it
    4. Maintain client ID context throughout the conversation session
    5. Use client ID to provide proactive service recommendations based on customer profile
    """,
    # All sub-agents and functions are provided in the 'tools' list
    sub_agents=[
        # tickets_agent,database_agent
    ],
    tools=[
        AgentTool(database_agent),
        AgentTool(network_diagnostics_agent),   
        AgentTool(commercial_agent),
        AgentTool(case_summary_agent),  
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

