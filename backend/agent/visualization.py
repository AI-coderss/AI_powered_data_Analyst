from agents import Agent
import json

from pydantic import BaseModel, validator

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

IMPORTANT: Your final output MUST be valid JSON. Do not include any explanatory text.
Output a JSON list of valid Highcharts configuration objects.

Your final response must be a pydantic model:
type should be "charts"
content should be ONLY the JSON list of valid Highcharts configuration objects.

Example valid output format:
{"type": "charts", "content": "[{\"chart\":{\"type\":\"bar\"},\"title\":{\"text\":\"Sample Chart\"},\"series\":[{\"data\":[1,2,3]}]}]"}
""",
    model="o3-mini",
    output_type=Step
)
