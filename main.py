
import chromadb 
from tqdm import tqdm
import warnings
warnings.filterwarnings("ignore")

import llm 
from database import database_utils
from youtube_utils import get_video_ids, get_video_transcript

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

    # Write in transcripts 
    get_video_transcript.get_transcripts_and_add_to_db(youtuber, connection = conn)