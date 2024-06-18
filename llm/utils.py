import json
import os 
import requests

from typing import List
from dotenv import load_dotenv
load_dotenv() 

API_KEY = os.environ['OPENAI_API_KEY']
with open('llm/CONFIG.json', 'r') as f:
    CONFIG = json.load(f)

def get_embedding(text_input:str) -> List[float]:
    """
    https://platform.openai.com/docs/guides/embeddings/what-are-embeddings
    """
    # Request headers, body, and URL
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {API_KEY}'
    }
    data = {
        "input": text_input,
        "model": CONFIG["EMBEDDING_MODEL"],
        "dimensions": CONFIG["EMBEDDING_DIMENSIONS"]
    }
    url = 'https://api.openai.com/v1/embeddings'
    
    # Get response and return the relevant parts only
    response = requests.post(url, headers=headers, json=data)
    return response.json()['data'][0]['embedding']

def get_openai_chat(message_list:list) -> str:
    """
    https://platform.openai.com/docs/api-reference/chat/create
    """
    api_url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + os.environ["OPENAI_API_KEY"]
    }
    data = {
        "model": CONFIG["LANGUAGE_MODEL"],
        "messages": message_list
    }
    response = requests.post(api_url, headers=headers, data=json.dumps(data))
    return response.json()['choices'][0]['message']['content']


def chat_with_gpt() -> None:
    """
    Chat with GPT crude logic 
    """
    messages = [{"role": "system","content": "You are a helpful assistant."},{"role": "assistant","content": "Hello!"}]

    while True: 
        user_input = input("User: ")
        if user_input == "STOP":
            break

        messages.append({'role':'user','content':user_input})
        result = get_openai_chat(messages)
        print(f"Bot: {result}")
        messages.append({'role':'assistant','content':result})
        
        