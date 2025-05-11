from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
import pandas as pd
import traceback
import openai
from dotenv import load_dotenv
from helpers.chart_generator import generate_highcharts_and_insights

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "https://ai-powered-data-analyst-dsah.onrender.com"}})


UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/upload", methods=["POST"])
def upload_file():
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

        result = generate_highcharts_and_insights(df)
        return jsonify(result)

    except Exception as e:
        traceback.print_exc()  # <--- Add this to print the full error
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
     app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5050)), threaded=True)