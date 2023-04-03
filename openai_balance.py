import json

import requests

from config import config_instance


def get_balance() -> str:
    url = 'https://api.openai.com/dashboard/billing/credit_grants'
    api_key = config_instance.openai_api_key
    headers = {
        "Authorization": "Bearer " + api_key,
        "Content-Type": "application/json"
    }
    response = requests.get(url, headers=headers)
    data = json.loads(response.text)
    total_used = data['total_used']
    return total_used
