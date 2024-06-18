
import chromadb 
from tqdm import tqdm
import warnings
warnings.filterwarnings("ignore")

from llm import utils as llm_utils
from llm import llm_config 
from database import database_utils
from youtube_utils import get_video_ids, get_video_transcript
from llm import chroma_embedding_wrapper 
from utils import clean_chroma_query_most_similar_document as clean 
from utils import cli_messages

if __name__ == '__main__':
    """ 
    This is the main flow of the script. 
    What you essentially see happen in the CLI and the main application logic is all here.    
    """

    # Print the greeting message
    cli_messages.print_greeting_message()


    youtuber = input("Enter the name of the youtuber you want to talk to: ").strip()
    print(f"Downloading data for {youtuber}...")

    # Make the SQLITE table connection 
    conn = database_utils.create_connection(db_name = './database/talk_to_youtuber_db.sqlite')

    # create the videos table 
    database_utils.create_table(conn)

    # Start downloading the video ids
    get_video_ids.get_videos(youtuber, conn)

    # Write in transcripts 
    get_video_transcript.get_transcripts_and_add_to_db(youtuber, conn)

    # # Download all their transcripts 
    all_videos = database_utils.get_videos_by_channel(conn, youtuber)

    # Start chroma client 
    # Create a new chroma/directory to from chroma data 
    client = chromadb.PersistentClient(path="chroma/")

    # Chroma collection 
    collection = client.get_or_create_collection(name="video_transcript_embeddings"
                                        ,metadata={"hnsw:space": "cosine"}
                                        ,embedding_function = chroma_embedding_wrapper.openai_ef)

    #Check if videos exist in the connection 
    collection_ids = collection.get()['ids']

    # Non over laps 
    # Keep only videos that are not already in the collection 
    non_overlapping_videos = [video_data for video_data in all_videos if video_data.video_id not in collection_ids]
    send_ids = [video_data.video_id for video_data in non_overlapping_videos]
    send_documents = [ str(video_data.video_title) + '--' + str(video_data.video_transcript) for video_data in non_overlapping_videos]
    send_documents = [document[0:30000] for document in send_documents] # Truncate for now 

    # Add the documents to the collection along with their ids 
    # Embeddings will be generated by chromadb using OpenAI
    print("Adding video transcripts to the Vector Database. These will be embedded, so this will take a while...")
    if send_ids:
        collection.add(
            ids = send_ids,
            documents = send_documents,
            metadatas=[{"channel_name": youtuber}] * len(send_ids)
        )
    print("Done! You can now talk to the youtuber by entering your query.")

    # LLM 
    cli_messages.print_llm_message()
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
            result_video = results['id']
            result_document = results['document']
            
            cli_messages.print_intercepting_message(result_document, result_video)

            user_input = cli_messages.intercept_string(user_input, result_document)

        messages.append({'role':'user','content':user_input})
        result = llm_utils.get_openai_chat(messages)
        print(f"Bot: {result}")
        messages.append({'role':'assistant','content':result})
        