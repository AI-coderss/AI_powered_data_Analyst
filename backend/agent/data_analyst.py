from agents import Agent

data_analyst_agent = Agent(
    name="Data Analyst",
    instructions="""
Analyze cleaned datasets to identify:
- Patterns and statistical trends
- Anomalies or outliers
- Correlations or significant groupings
- Business-relevant performance segments
Provide 4–6 clearly structured findings in text format.
""",
    model="gpt-4o"
)
