from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
import pandas as pd
import traceback
import openai
import json
from dotenv import load_dotenv
# Import the agents
from agent.data_processor import data_processor_agent
from agent.data_analyst import data_analyst_agent
from agent.visualization import visualization_agent
from agent.insight_generator import insight_generator_agent
from agents import Runner

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})


UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/upload", methods=["POST"])
async def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    try:
        # Read uploaded file into DataFrame
        if filename.endswith(".csv"):
            df = pd.read_csv(filepath)
        elif filename.endswith((".xls", ".xlsx")):
            df = pd.read_excel(filepath)
        else:
            return jsonify({"error": "Unsupported file format"}), 400

        # Step 1: Process data with Data Processor agent
        df_json = df.head(100).to_json(orient="records")
        #print(df_json)

        
         # Run all the async agent processing steps
        processed_data = await Runner.run(data_processor_agent, f"Clean and preprocess the following dataset: {df_json}")
        
        # # Step 2: Analyze data with Data Analyst agent
        analysis = await Runner.run(data_analyst_agent, f"Analyze this processed dataset and provide insights: {processed_data}")
        
        # # Step 3: Generate visualizations with Visualization Specialist agent
        visualizations = await Runner.run(visualization_agent, f"""
                You are given a tabular dataset sample below. Your task is to:

                1. Analyze the data thoroughly and suggest multiple Highcharts JS configurations in JSON format to cover every significant aspect of the data.
                2. Make the charts interactive with features such as clickable points, drilldowns, zooming, and dynamic updates.
                3. Ensure all charts use consistent categories where applicable (e.g., "Region", "Department") to allow cross-filtering between charts.
                4. Include animations and interactive widgets to enhance user engagement.
                5. Ensure proper alignment and responsive layout for embedding in a dashboard.

                ### Dataset Sample:
                {analysis}

                ### Output format:
                {{
                "charts": [ ... ],   // list of Highcharts JSON config objects
                }}

                Respond ONLY with a pure JSON object. Do NOT include markdown, comments, or explanation.
                """)
        
         # Step 4: Generate final insights with Insight Generator agent
        insights = await Runner.run(insight_generator_agent, f"Generate insights and recommendations based on this data: \
                     \nData: {processed_data}")
        
        

        # Modified result to include both visualizations and insights
        vis_data = json.loads(visualizations.final_output)
        result = {
            "charts": vis_data["charts"],
            "insights": insights.final_output
        }
        

        return jsonify(result)
        


    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

@app.route("/chat", methods=["POST"])
def chat_with_ai():
    data = request.json
    prompt = data.get("prompt")
    charts = data.get("charts")

    message = f"""
You are an AI BI analyst. A user asked:
"{prompt}"

The current dashboard charts are:
{charts}

Give a markdown summary of insights based on the data and the question.
"""

    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[{ "role": "user", "content": message }],
        temperature=0.5,
    )
    reply = response.choices[0].message.content.strip()
    return jsonify({ "response": reply })


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5050, debug=True)