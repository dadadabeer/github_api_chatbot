# chatbot.py
import json
import logging
import openai
import os
from dotenv import load_dotenv
load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

with open("github_api_full_documentation.json") as file:
    documentation_data = json.load(file)

# Function to find the most relevant section based on keywords in the query
def find_relevant_section(query):
    """
    Finds the most relevant section in the documentation based on keywords in the user's query.

    Args:
        query (str): The user's query to search for relevant documentation.

    Returns:
        tuple: A tuple containing the section title and text of the most relevant section, 
               or None if no relevant section is found.
    """

    relevant_sections = []
    query_lower = query.lower()
    
    # Check each section in the documentation for relevance
    for _, content in documentation_data.items():
        for section_title, section_text in content.items():
            if any(keyword in query_lower for keyword in section_title.lower().split()):
                relevant_sections.append((section_title, section_text))
                break  # Stop after finding a relevant match in this section
    
    # Return the most relevant section
    if relevant_sections:
        return relevant_sections[0]  # You can return the top match, or all matches if desired
    else:
        return None

# Function to generate a response based on the user's query
def generate_response(query):
    """
    Generates a structured response based on the user's query by using the OpenAI API.

    Args:
        query (str): The user's query to search for relevant documentation and generate a response.

    Returns:
        str: A structured response containing relevant information from the documentation, 
             or an error message if the information cannot be retrieved.
    """
    try:
        # Find the relevant section in the documentation
        relevant_section = find_relevant_section(query)
        
        if relevant_section:
            section_title, section_text = relevant_section
            # Construct a link based on the section title
            # link = f"https://docs.github.com/en/rest/{section_title.replace(' ', '-').lower()}"
            
            # Refined prompt for a more structured response
            prompt = (
                f"Based on the following GitHub API documentation section:\n\n"
                f"Title: {section_title}\n\n"
                f"Content: {section_text}\n\n"
                f"Please provide a structured response to the user's query below. "
                f"Format the answer as follows:\n\n"
                f"**Section Title**: <section_title>\n"
                f"**Relevant Information**:\n\n"
                f"1. Summarize key points in clear, concise bullets or numbered steps.\n"
                f"2. Ensure the answer is directly related to the query.\n\n"
                f"User's query: {query}"
            )
            
            # Use ChatCompletion API with GPT-4 model
            response = openai.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant for GitHub API documentation. Answer the user's query in a structured format with a section title, link, and relevant content in a readable format."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=200  # Adjust based on the response length
            )
            # Extract the generated message content
            return response.choices[0].message.content.strip()
        else:
            return "I'm sorry, I couldn't find relevant information in the documentation."
    except Exception as e:
        # Log the full traceback of the exception for easier debugging
        import traceback
        print("Error in generate_response:")
        print(traceback.format_exc())
        return f"Error: {str(e)}"

