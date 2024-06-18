
import chromadb 
from tqdm import tqdm
import warnings
warnings.filterwarnings("ignore")

from llm import utils as llm_utils
from llm import llm_config 
from database import database_utils
from youtube_utils import get_video_ids, get_video_transcript
from chroma_utils import chroma_embedding_wrapper 
from utils import clean_chroma_query_most_similar_document as clean 

if __name__ == '__main__':
    """ 
    This is the main flow of the script. 
    What you essentially see happen in the CLI and the main application logic is all here.    
    """

    print("Hey Welcome to Talk to Youtuber")
    youtuber = input("Enter the name of the youtuber you want to talk to: ")
    print(f"Downloading data for {youtuber}...")

    # Make the SQLITE table connection 
    conn = database_utils.create_connection(db_name = './database/talk_to_youtuber_db.sqlite')

    # create the videos table 
    database_utils.create_table(conn)

    # Start downloading the video ids
    get_video_ids.get_videos(youtuber, connection = conn)

    # # Download all their transcripts 
    all_videos = database_utils.get_videos_by_channel(conn, channel_name = youtuber)
    video_ids = [video_data.video_id for video_data in all_videos]

    # Write in transcripts 
    get_video_transcript.get_transcripts_and_add_to_db(youtuber, connection = conn)

    # Start chroma client 
    # Create a new chroma/directory to from chroma data 
    client = chromadb.PersistentClient(path="chroma/")

    # Chroma collection 
    collection = client.get_or_create_collection(name="video_transcript_embeddings"
                                        ,metadata={"hnsw:space": "cosine"}
                                        ,embedding_function = chroma_embedding_wrapper.ChromaEmbeddingWrapper())

    #Check if videos exist in the connection 
    collection_ids = collection.get()['ids']

    # Non over laps 
    # Keep only videos that are not already in the collection 
    non_overlapping_videos = [video_data for video_data in all_videos if video_data.video_id not in collection_ids]
    send_ids = [video_data.video_id for video_data in non_overlapping_videos]
    send_documents = [str(video_data.video_title) + ' ' + str(video_data.video_transcript) for video_data in all_videos]

    # Add the documents to the collection along with their ids 
    # Embeddings will be generated by chromadb using OpenAI
    print("Adding video transcripts to the Vector Database. These will be embedded, so this will take a while...")
    collection.add(
        ids = send_ids,
        documents = send_documents,
        metadatas=[{"channel_name": youtuber}] * len(send_ids)
    )
    print("Done! You can now talk to the youtuber by entering your query.")

    # TODO 
    # Add in the chat with RAG 
    messages = llm_config.messages
    while True: 
        user_input = input("User: ")

        # RAG Logic 
        if '??' in user_input:
            # Query chroma with users question 
            matched_document = collection.query(
                                    query_texts=[user_input], 
                                    n_results=1 ,
                                    where={"channel_name": youtuber}
                                )
            results = clean.clean_chroma_query_most_similar_document(matched_document)
            result_video = f"https://www.youtube.com/watch?v={results['id']}"
            result_document = results['document']
            
            print(f"\n\n Intercepting query with additional contet:\n\nContext is\m {result_document}\n\n") 

            user_input += "\nSome additional context"
            user_input += "result_document"
            user_input += "---------------------"

        messages.append({'role':'user','content':user_input})
        result = llm_utils.get_openai_chat(messages)
        print(f"Bot: {result}")
        messages.append({'role':'assistant','content':result})
        