def clean_chroma_query_most_similar_document(query_results: dict) -> dict:
    """
    Clean the most similar document from a Chroma query.
    
    Parameters:
    query_results (dict): A dictionary containing 'distances', 'documents', and 'ids'.
    
    Returns:
    dict: A dictionary containing the 'document' and its corresponding 'id'.
    """
    distances = query_results['distances'][0]
    documents = query_results['documents'][0]
    metadatas = query_results['metadatas'][0]


    document = documents[0]
    video_id = query_results['ids'][0][0].split('_')[0]
    title = metadatas[0]['title']

    # Create a dictionary with 'document' and 'id'
    most_similar_document = {
        'id':video_id,
        'document': document,
        'title': title
    }

    return most_similar_document

def chunk_text(text, chunk_size=1000):
    words = text.split()
    return [' '.join(words[i:i+chunk_size]) for i in range(0, len(words), chunk_size)]