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
    ids = query_results['ids'][0]

    # Create a list of tuples (id, document, distance)
    results = list(zip(ids, documents, distances))

    # Get the most similar document (minimum distance)
    most_similar_result = min(results, key=lambda x: x[2])

    # Create a dictionary with 'document' and 'id'
    most_similar_document = {
        'id': most_similar_result[0],
        'document': most_similar_result[1]
    }

    return most_similar_document
