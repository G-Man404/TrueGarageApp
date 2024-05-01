import os
from dotenv import load_dotenv

load_dotenv()

token = os.getenv('TG_TOKEN')

api_key = os.getenv('API_KEY')

api_url = os.getenv('API_URL')

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Api-key {api_key}"
}