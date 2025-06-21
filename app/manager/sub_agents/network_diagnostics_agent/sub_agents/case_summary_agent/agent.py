from google.adk.agents import Agent

case_summary_agent = Agent(
    # A unique name for the agent.
    name="case_summary_agent",
    model="gemini-2.0-flash-exp",
    description="Agent that summarizes a conversation.",
    instruction="""
    You are a helpful assistant that summarizes the conversation provided.
    Your goal is to create a concise summary of the key points, decisions, and action items from the conversation.
    Do not add any information that was not in the original conversation.
    Keep the summary brief and to the point.
    """,
    tools=[],
)
