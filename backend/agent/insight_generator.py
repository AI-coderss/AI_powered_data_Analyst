from agents import Agent

from pydantic import BaseModel

class Step(BaseModel):
    type: str
    content: str


insight_generator_agent = Agent(
    name="Insight Generator",
    instructions="""
Synthesize all data and visuals into a Markdown report.
- Include 3–5 business insights
- Use bullet points or short paragraphs
- Follow each insight with a recommendation
- Avoid technical language
Return the result as clean Markdown text.
IMPORTANT: Always format your final response as a pydantic model:
type should be "insights"
content should be the insights and recommendations
""",
    model="gpt-4o",
    output_type=Step
)
