from agents import Agent
from data_analyst import data_analyst_agent
from insight_generator import insight_generator_agent   
from visualization import visualization_agent

supervisor_agent = Agent(
    name="Supervisor Agent",
    instruction="""
        You are a supervisor agent. You have access to multiple agents, such as data_analyst agent, visualization agent, and insight_generator agent.
        When you recieve a request from the user, handoff to relevant agent based on request.
        If the request is about data analysis, handoff to data_analyst agent.
        If the request is about generating insights, handoff to insight_generator agent.
        If the request is about visualizing data, handoff to visualization agent.
    """,
    handoffs=[data_analyst_agent, insight_generator_agent, visualization_agent]
)