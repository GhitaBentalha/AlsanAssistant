# chatbot/utils.py

import requests

API_URL = "https://api.exemple.com/chatbot"  # Remplacez par l'URL réelle
API_KEY = "votre_clé_api"  # Remplacez par votre clé API

def envoyer_message(message):
    headers = {
        'Authorization': f'Bearer {API_KEY}',
        'Content-Type': 'application/json',
    }
    payload = {
        'message': message
    }
    response = requests.post(API_URL, headers=headers, json=payload)
    
    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()
