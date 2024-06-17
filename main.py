
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
    conn = database_utils.create_connection()

    # create the videos table 
    database_utils.create_table(conn)

    # Start downloading the video ids
    get_video_ids.get_videos(youtuber, connection = conn)

    # # Download all their transcripts 
    all_videos = database_utils.get_videos_by_channel(conn, channel_name = youtuber)

    print(all_videos)
    for video in tqdm(all_videos):
        try:
            video_id = video[1]
            transcript = get_video_transcript.get_video_transcript(video_id)
        except KeyboardInterrupt:
            print("You stopped the process")
            break