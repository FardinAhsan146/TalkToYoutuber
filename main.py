
import chromadb 
from tqdm import tqdm

import llm 
from database import database_utils
from youtube_utils import get_video_ids
if __name__ == '__main__':
    print("Hey Welcome to Talk to Youtuber")
    youtuber = input("Enter the name of the youtuber you want to talk to: ")
    print(f"Downloading data for {youtuber}...")

    # Make the SQLITE table connection 
    conn = database_utils.create_connection()

    # create the videos table 
    database_utils.create_table(conn)

    # Start downloading the video ids
    get_video_ids.get_videos(youtuber, connection = conn)

    # # Download all their transcripts 
    # all_videos = sqlite.get_videos_by_channel(youtuber)
    # for video in tqdm(all_videos):
    #     transcript = youtube_utils.get_video_transcript()