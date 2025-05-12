import asyncio
from agents import Agent, Runner, handoff
from agent.data_processor import data_processor_agent
from agent.data_analyst import data_analyst_agent
from agent.visualization import visualization_agent
from agent.insight_generator import insight_generator_agent

# Define the orchestrator agent
orchestrator_agent = Agent(
    name="Orchestrator",
    instructions="""
You are responsible for coordinating the data analysis workflow:
1. Receive the raw dataset.
2. Delegate to the Data Processor Agent to clean the data.
3. Pass the cleaned data to the Data Analyst Agent for analysis.
4. Send the analysis results to the Visualization Agent to generate charts.
5. Provide the visualizations to the Insight Generator Agent to create summaries and recommendations.
""",
    model="gpt-4o",
    handoffs=[
        data_processor_agent,
        handoff(data_analyst_agent),
        handoff(visualization_agent),
        handoff(insight_generator_agent)
    ]
)

# Function to run the orchestrator
def run_workflow(dataset):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    result = loop.run_until_complete(Runner.run(orchestrator_agent, input=dataset))
    loop.close()
    return result.final_output

