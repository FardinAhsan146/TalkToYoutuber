import chromadb 

import os, sys, json 
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
sys.path.append(parent_dir)

import llm 

class ChromaEmbeddingWrapper(chromadb.EmbeddingFunction):
    """ Interface for ChromaDB to use the OpenAI API for embeddings """
    def __call__(self, input: chromadb.Documents) -> chromadb.Embeddings:
        return [llm.utils.get_embedding(text) for text in input]
    