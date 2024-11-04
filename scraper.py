import requests
from bs4 import BeautifulSoup
import json
import time

# Base URL for the main page and to check for relevant links
base_url = "https://docs.github.com"
main_url = f"{base_url}/en/rest/"

# Function to extract all documentation links from the main page
def get_section_links(main_url):
    response = requests.get(main_url)
    soup = BeautifulSoup(response.content, "html.parser")
    
    # Find all links within the main content area
    links = []
    for link in soup.find_all("a", href=True):
        href = link['href']
        # Collect links that start with '/en/rest/' (internal links for REST API documentation)
        if href.startswith("/en/rest/") and href not in links:
            links.append(base_url + href)
    return links

# Function to scrape content from each section page
def scrape_section(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    
    # Dictionary to store content
    section_data = {}

    # Use similar logic as before to find headers and content
    sections = soup.find_all("h2")  # or adjust based on the actual HTML structure
    
    for section in sections:
        title = section.get_text().strip()
        
        # Find the content associated with this section
        content = []
        for sibling in section.find_next_siblings():
            if sibling.name == "h2":  # Stop at the next main section
                break
            content.append(sibling.get_text().strip())
        
        # Add content to dictionary
        section_data[title] = " ".join(content)

    return section_data

# Collect all section links
section_links = get_section_links(main_url)

# Dictionary to hold all documentation data
documentation_data = {}

# Loop through each link, scrape its content, and add to our documentation_data dictionary
for link in section_links:
    print(f"Scraping {link}")
    section_content = scrape_section(link)
    documentation_data[link] = section_content
    time.sleep(1)  # Be respectful by adding a delay between requests

# Save to a JSON file
with open("github_api_full_documentation.json", "w") as file:
    json.dump(documentation_data, file, indent=4)

print("All sections scraped and saved to github_api_full_documentation.json")
