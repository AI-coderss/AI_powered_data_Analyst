from agents import Agent

visualization_agent = Agent(
    name="Visualization Specialist",
    instructions="""
Create 4–6 interactive Highcharts JSON chart configurations based on analysis.
Use varied chart types (bar, column, pie, heatmap, line, stacked bar).
Ensure each chart:
- Has clear axis labels and categories
- Supports tooltips, click interactions, and drilldowns
- Highlights the insights clearly
Output a JSON list of valid Highcharts configuration objects.
""",
    model="o3-mini"
)
