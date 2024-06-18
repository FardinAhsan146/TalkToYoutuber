
import chromadb 
from tqdm import tqdm
import warnings
warnings.filterwarnings("ignore")

import llm 
from database import database_utils
from youtube_utils import get_video_ids, get_video_transcript
from chroma_utils import chroma_embedding_wrapper 

if __name__ == '__main__':
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
        documents = send_documents
    )
    print("Done! You can now talk to the youtuber by entering your query.")

    # TODO 
    # Add in the chat with RAG 