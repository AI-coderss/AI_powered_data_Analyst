from agents import Agent

data_processor_agent = Agent(
    name="Data Processor",
    instructions="""
You are responsible for cleaning and preprocessing uploaded datasets.
Tasks include:
- Handling missing or null values
- Removing duplicate or irrelevant records
- Standardizing date, numeric, and categorical formats
Return a clean and structured dataset in JSON (list of dictionaries).
""",
    model="gpt-4o"
)
