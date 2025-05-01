import os
from dotenv import load_dotenv

load_dotenv()

# API Configurations
openai_api_key = os.getenv('OPENAI_API_KEY')
anthropic_api_key = os.getenv('ANTHROPIC_API_KEY')
google_api_key = os.getenv('GOOGLE_API_KEY')

if openai_api_key:
    print(f"OpenAI API Key exists and begins {openai_api_key[:8]}")
else:
    print("OpenAI API Key not set")
    
if anthropic_api_key:
    print(f"Anthropic API Key exists and begins {anthropic_api_key[:7]}")
else:
    print("Anthropic API Key not set")

if google_api_key:
    print(f"Google API Key exists and begins {google_api_key[:8]}")
else:
    print("Google API Key not set")


# Scraping configurations
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}
REQUEST_TIMEOUT = 30  # seconds
MAX_RETRIES = 3

# Search engine API keys (optional, for competitor finding)
SERPAPI_KEY = os.getenv("SERPAPI_KEY")

# Analysis settings
MAX_COMPETITORS = 5
INDUSTRY_SECTORS = [
    "Technology", "Healthcare", "Finance", "Retail", "Manufacturing", 
    "Education", "Entertainment", "Food & Beverage", "Transportation", "Energy"
]
