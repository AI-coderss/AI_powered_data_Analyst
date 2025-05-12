from openai import OpenAI
import os
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_highcharts_and_insights(df):
    sample = df.head(100).to_dict(orient="records")

    # Assistant prompt
    o3_assistant_prompt = (
        "You are a data analyst AI assistant who generates comprehensive Highcharts JSON configurations and detailed markdown insights from datasets. "
        "Your goal is to provide multiple, fully interactive charts that cover all aspects of the data without omitting any important details."
    )

    # User prompt with dataset
    o3_user_prompt = f"""
You are given a tabular dataset sample below. Your task is to:

1. Analyze the data thoroughly and suggest multiple Highcharts JS configurations in JSON format to cover every significant aspect of the data.
2. Make the charts interactive with features such as clickable points, drilldowns, zooming, and dynamic updates.
3. Ensure all charts use consistent categories where applicable (e.g., "Region", "Department") to allow cross-filtering between charts.
4. Include animations and interactive widgets to enhance user engagement.
5. Write a detailed insights report along with recommendations.
6. Ensure proper alignment and responsive layout for embedding in a dashboard.

### Dataset Sample:
{sample}

### Output format:
{{
  "charts": [ ... ],   // list of Highcharts JSON config objects
  "insights_md": "..." // markdown bullet points or summary
}}

Respond ONLY with a pure JSON object. Do NOT include markdown, comments, or explanation.
"""

    try:
        # API call to o3-mini with reasoning effort
        response = client.chat.completions.create(
            model="o3-mini",
            messages=[
                {"role": "assistant", "content": o3_assistant_prompt},
                {"role": "user", "content": o3_user_prompt}
            ],
            reasoning_effort="high",
            timeout=20  # Optional timeout to avoid hanging on Render
        )

        content = response.choices[0].message.content.strip()

        try:
            return json.loads(content)
        except json.JSONDecodeError as e:
            print("⚠️ JSON decoding failed. Raw content:")
            print(content)
            return {
                "charts": [],
                "insights_md": "⚠️ Failed to parse OpenAI response. Please try again.",
                "error": "Invalid JSON returned from model."
            }

    except Exception as e:
        import traceback
        traceback.print_exc()
        return {
            "charts": [],
            "insights_md": "⚠️ OpenAI API call failed. Check logs or try again.",
            "error": str(e)
        }




