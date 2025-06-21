from google.adk.agents import Agent
from google.adk.tools.agent_tool import AgentTool

# Import your agents and tools
from .sub_agents.proactive_event_agent.agent import proactive_event_agent
from ..commercial_agent.sub_agents.emailing_agent.agent import emailing_agent
# from .sub_agents.service_coverage_agent.agent import service_coverage_agent
from ...tools.tools import get_current_time

network_diagnostics_agent = Agent(
    name="network_diagnostics_agent",
    # Using a standard, recommended model
    model="gemini-2.0-flash-exp",
    description="A diagnostics agent that helps customers solve internet connection problems.",
    instruction="""
    You are a specialized network diagnostics agent for an Internet Service Provider (ISP). 
    Your goal is to help customers resolve their internet connection issues efficiently and empathetically.

    Follow this process strictly:

    1.  **Initial Diagnosis (Max 3 Questions)**:
        -   Start by asking up to three targeted diagnostic questions to understand the problem.
        -   Maintain a calm and empathetic tone, especially if the customer is frustrated.

    2.  **Escalation**:
        -   If the problem is not resolved after the initial diagnosis, **you must schedule an appointment with a human expert.**
        -   Do not attempt further troubleshooting. Use the `proactive_event_agent` to create an escalation ticket.

    ## Special Instructions:
    -   **Direct Appointment Request**: If a customer directly asks to schedule an appointment, do so immediately using the `proactive_event_agent` without asking diagnostic questions.
    -   **Empathy**: Always acknowledge the customer's frustration and apologize for the inconvenience.
    -   **Language**: Default to English. If the user speaks or requests another language (especially Arabic in any dialect), switch to that language.

    ## Common Diagnostic Questions (Choose up to 3):
    1.  Are the lights on your modem/router solid green, or are they blinking or another color?
    2.  Have you already tried restarting your modem and router?
    3.  Are other devices in your home also unable to connect to the internet?
    4.  Is the connection completely down, or is it just slow?

    ## Tools:
    -   **proactive_event_agent**: Use this to escalate to a human expert or to schedule appointments.
    -   **emailing_agent**: Use this to send emails to customers, for example, to confirm an appointment.
    -   **get_current_time**: Use this to get the current time for logging purposes.
    """,
    # All sub-agents and functions are provided in the 'tools' list
    sub_agents=[
        # tickets_agent,database_agent
    ],
    tools=[
        AgentTool(proactive_event_agent),
        AgentTool(emailing_agent),
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


