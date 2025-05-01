import os
from dotenv import load_dotenv

load_dotenv()

# API Configurations
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
CLAUDE_MODEL = "claude-3-opus-20240229"  # Select appropriate model

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
