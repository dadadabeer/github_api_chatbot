GitHub API Documentation Chatbot

This chatbot is designed to answer questions about the GitHub API by leveraging structured documentation data stored in a JSON file and OpenAI's language model to generate responses.

Project Structure:

github_api_full_documentation.json:

Description: This JSON file contains structured data extracted from GitHub’s REST API documentation, organized by sections.

How It Was Scraped: The data was scraped from GitHub's documentation pages using Python’s requests and BeautifulSoup libraries. 
Relevant sections and content were identified and stored in JSON format, allowing the chatbot to look up information based on user queries.

app.py:

Description: This file contains the Flask application, which serves as the API backend for the chatbot. It defines a /query endpoint that accepts POST requests with a JSON payload containing a user's query.

Functionality: When a request is received, app.py calls the generate_response function from chatbot.py to process the query and return a structured response.

chatbot.py:

Description: This file contains the main logic for the chatbot, including:
find_relevant_section: Searches the JSON documentation data for the section most relevant to the user’s query.
generate_response: Uses OpenAI’s API to generate a structured answer based on the relevant section and the query.

How to Run the Application:

pip install flask openai python-dotenv

Add your OpenAI API key to a .env file:

OPENAI_API_KEY= your_openai_api_key


Start the Flask Server:

Run the Flask app by executing:

python app.py

The server will start on http://127.0.0.1:5000.

Interact with the Chatbot:

Interact on the local server or Use a tool like curl or Postman to send a POST request to http://127.0.0.1:5000/query.


Example Request:

curl -X POST http://127.0.0.1:5000/query -H "Content-Type: application/json" -d '{"query": "How do I authenticate with the GitHub API?"}'

The chatbot will return a structured response based on the query, using the information in github_api_full_documentation.json.
