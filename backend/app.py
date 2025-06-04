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
from agent.supervisor_agent import supervisor_agent
from agents import Runner
from pydantic import BaseModel

class Step(BaseModel):
    type: str
    output: str

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "https://ai-powered-data-analyst-2l0a.onrender.com"}})


UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Add a global variable to store the latest processed data
# This is a simple solution for development - for production, consider a database
latest_processed_data = {
    "raw_data": None,
    "processed_data": None,
    "analysis": None,
    "charts": None,
    "insights": None
}

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

        # Store the raw data
        latest_processed_data["raw_data"] = df.head(100).to_json(orient="records")
        df_json = latest_processed_data["raw_data"]

        # Step 1: Process data with Data Processor agent
        processed_data = await Runner.run(data_processor_agent, f"Clean and preprocess the following dataset: {df_json}")
        latest_processed_data["processed_data"] = processed_data
        
        # Step 2: Analyze data with Data Analyst agent
        analysis = await Runner.run(data_analyst_agent, f"Analyze this processed dataset and provide insights: {processed_data.final_output}")
        latest_processed_data["analysis"] = analysis.final_output
        
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
        
        # Store the visualization data
        charts_content = visualizations.final_output.content
        charts_json = json.loads(charts_content)
        latest_processed_data["charts"] = charts_json
        
        # Store the insights
        latest_processed_data["insights"] = insights.final_output.content
        
        results = {
            "charts": latest_processed_data["charts"],
            "insights": latest_processed_data["insights"]
        }
        return jsonify(results)
        


    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

@app.route("/chat", methods=["POST"])
async def chat_with_ai():
    try:
        data = request.json
        prompt = data.get("prompt")
        
        # If no data provided by client, use our stored data
        dataset = latest_processed_data["analysis"]
        visualizations = latest_processed_data["charts"]
        insights = latest_processed_data["insights"]
        
        # If we still don't have data, inform the user
        if not dataset:
            return jsonify({"response": "Please upload a dataset first or provide data in your request."}), 400

        reply = await Runner.run(supervisor_agent, 
                         f"""The current dashboard data is: {dataset}
                         the current visualizations are: {visualizations}
                         the current insights are: {insights}  
                         the user prompt is: {prompt}
                        
                        
                         """
                         )
        print("reply", reply.final_output.type)

        #process output based on type
        output = reply.final_output.content

        if reply.final_output.type == "charts":
            output = json.loads(output)
        
        # Convert Pydantic model to dictionary before jsonifying
        response_dict = {
            "type": reply.final_output.type,
            "reply": output
        }
        
        # Return the dictionary instead of the Pydantic model
        return jsonify(response_dict)

    except Exception as e:
        print(f"Error in chat endpoint: {str(e)}")
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5050, debug=True)