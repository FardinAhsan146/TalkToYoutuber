import chromadb 
from tqdm import tqdm
import warnings
warnings.filterwarnings("ignore")

from llm import utils as llm_utils
from llm import llm_config 
from database import database_utils
from youtube_utils import get_video_ids, get_video_transcript
from llm import chroma_embedding_wrapper 
from utils import utils 
from utils import cli_messages
from concurrent.futures import ThreadPoolExecutor, as_completed


def process_video(video_data, collection, youtuber):
    full_text = f"{video_data.video_transcript}"
    chunks = utils.chunk_text(full_text)
    
    for i, chunk in enumerate(chunks):
        chunk_id = f"{video_data.video_id}_{i}" # natural key
        collection.add(
            ids=[chunk_id],
            documents=[chunk],
            metadatas=[{"channel_name": youtuber, "title": video_data.video_title}]
        )
    return video_data.video_id

if __name__ == '__main__':
    """ 
    This is the main flow of the script. 
    What you essentially see happen in the CLI and the main application logic is all here.    
    """

    # Print the greeting message
    cli_messages.print_greeting_message()

    youtuber = input("Enter the name of the youtuber you want to talk to: ").strip()

    # Make the SQLITE table connection 
    conn = database_utils.create_connection(db_name = './database/talk_to_youtuber_db.sqlite')

    # create the videos table 
    database_utils.create_table(conn)

    # Start downloading the video ids
    get_video_ids.get_videos(youtuber, conn)

    # Write in transcripts 
    get_video_transcript.get_transcripts_and_add_to_db(youtuber, conn)

    # Download all their transcripts 
    all_videos = database_utils.get_videos_by_channel(conn, youtuber)

    # Start chroma client 
    # Create a new chroma/directory to from chroma data 
    client = chromadb.PersistentClient(path="chroma/")

    # Chroma collection 
    collection = client.get_or_create_collection(name="video_transcript_embeddings",
                                                 metadata={"hnsw:space": "cosine"},
                                                 embedding_function=chroma_embedding_wrapper.openai_ef)

    # Check if videos exist in the connection 
    collection_ids = collection.get()['ids']

    # Non overlaps 
    # Keep only videos that are not already in the collection 
    non_overlapping_videos = [video_data for video_data in all_videos if video_data.video_id not in collection_ids]

    with ThreadPoolExecutor() as executor:
        futures = []
        for video_data in non_overlapping_videos:
            future = executor.submit(process_video, video_data, collection, youtuber)
            futures.append(future)
        
        # Use tqdm to show progress
        for future in tqdm(as_completed(futures), total=len(futures), desc="Embedding and adding to vector DB"):
            video_id = future.result()

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
                n_results=1,
                where={"channel_name": youtuber}
            )
            results = utils.clean_chroma_query_most_similar_document(matched_document)
            result_video = results['id']
            result_document = results['document']
            result_title = results['title']
            
            cli_messages.print_intercepting_message(result_document, result_video, result_title)

            user_input = cli_messages.intercept_string(user_input, result_document)

        messages.append({'role':'user','content':user_input})
        result = llm_utils.get_openai_chat(messages)
        print(f"\nBot: {result}\n")
        messages.append({'role':'assistant','content':result})