import os
import sys
from sqlite3 import Connection
import youtube_transcript_api 
import concurrent.futures
from tqdm import tqdm 

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
sys.path.append(parent_dir)
from database.database_utils import update_video_transcript, create_connection, get_videos_by_channel, check_transcript_attempted

def get_video_transcript(video_id: str) -> str | None:
    """
    Get the transcript of a YouTube video given its video_id. 
    Will clean it up and turn it into a document here. 
    The api doesn't return any other USEFUL information.
    """
    try:
        transcript = youtube_transcript_api.YouTubeTranscriptApi.get_transcript(video_id)
        text = ' '.join([line['text'] for line in transcript])
        return text 
    except youtube_transcript_api._errors.TranscriptsDisabled:
        return None

def get_transcripts_and_add_to_db(channel_name:str, connection: Connection):
    """
    We need to ge the transcripts and populate the local store  
    """
    print(f"Getting transcripts for {channel_name}...")
    all_videos = get_videos_by_channel(connection, channel_name = channel_name)
    for video in tqdm(all_videos):
        video_id = video.video_id # video ID field 

        # This should save us some time 
        if check_transcript_attempted(connection, video_id):
            continue 

        transcript = get_video_transcript(video_id)
        if transcript:
            update_video_transcript(connection, video_id, transcript)
    print(f"Transcripts for {channel_name} have been updated.")

