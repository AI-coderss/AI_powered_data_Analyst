from agents import Agent

insight_generator_agent = Agent(
    name="Insight Generator",
    instructions="""
Synthesize all data and visuals into a Markdown report.
- Include 3–5 business insights
- Use bullet points or short paragraphs
- Follow each insight with a recommendation
- Avoid technical language
Return the result as clean Markdown text.
""",
    model="gpt-4o"
)
