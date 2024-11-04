# app.py
from flask import Flask, request, jsonify, render_template
from chatbot import generate_response
from dotenv import load_dotenv
load_dotenv()



app = Flask(__name__)

@app.route('/')
def home():
    """Render the home page."""
    return render_template('index.html')

# Endpoint for the chatbot API
@app.route('/query', methods=['POST'])
def query():
    """Endpoint to receive queries and return responses from the chatbot."""
    data = request.json
    query = data.get("query", "")
    answer = generate_response(query)
    return jsonify({"response": answer})

if __name__ == '__main__':
    app.run(port=5000)
