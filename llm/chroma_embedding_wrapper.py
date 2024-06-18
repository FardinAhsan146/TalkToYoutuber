import os,json 
import chromadb 
import chromadb.utils.embedding_functions as embedding_functions
from dotenv import load_dotenv
load_dotenv() 

API_KEY = os.environ['OPENAI_API_KEY']
with open('llm/CONFIG.json', 'r') as f:
    CONFIG = json.load(f)

openai_ef = embedding_functions.OpenAIEmbeddingFunction(
                api_key=API_KEY,
                model_name=CONFIG["EMBEDDING_MODEL"]
            )
