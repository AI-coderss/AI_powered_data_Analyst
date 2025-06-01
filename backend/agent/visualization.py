from agents import Agent

from pydantic import BaseModel

class Step(BaseModel):
    type: str
    content: str

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
IMPORTANT: Always format your final response as a pydantic model:
type should be "charts"
content should be the JSON list of valid Highcharts configuration objects.
""",
    model="o3-mini",
    output_type=Step
)
