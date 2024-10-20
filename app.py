from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os

import google.generativeai as genai

load_dotenv()

app = Flask(__name__)
CORS(app)

genai.configure(api_key=os.environ["GEMINI_API_KEY"])

model = genai.GenerativeModel("gemini-1.5-flash")
chat = model.start_chat(
  history=[
    {"role": "model", "parts": ["Hello! How can I assist you today?"]},
  ]
)

@app.route('/send_message', methods=['POST'])
def send_message():
    data = request.get_json()
    user_message = data.get('message')
    
    if user_message:
        response = chat.send_message(user_message)
        return jsonify({'reply': response.text})
    else:
        return jsonify({'error': 'No message provided'}), 400

if __name__ == '__main__':
    app.run(debug=True)
