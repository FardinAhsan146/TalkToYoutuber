import os
import sys
from sqlite3 import Connection
import youtube_transcript_api 
from tqdm import tqdm 

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
sys.path.append(parent_dir)
from database.database_utils import update_video_transcript, get_videos_by_channel, check_transcript_attempted
from concurrent.futures import ThreadPoolExecutor, as_completed

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
    except youtube_transcript_api._errors.NoTranscriptFound:
        return None 

def get_transcripts_and_add_to_db(channel_name:str, connection: Connection):
    """
    Get and store transcripts for all videos of a given channel concurrently.
    """
    all_videos = get_videos_by_channel(connection, channel_name)
    transcripts_dict = {}

    # Prepare the list of videos to process
    videos_to_process = []

    for video in all_videos:
        video_id = video.video_id
        if not check_transcript_attempted(connection, video_id):
            videos_to_process.append(video_id)

    # Multi thread this shit 
    with ThreadPoolExecutor(max_workers=100) as executor:
        future_to_video_id = {executor.submit(get_video_transcript, video_id): video_id for video_id in videos_to_process}
        for future in tqdm(as_completed(future_to_video_id), total=len(videos_to_process), desc = f"Downloading transcripts for {channel_name}."):
            video_id = future_to_video_id[future]
            transcript = future.result()
            if transcript:
                transcripts_dict[video_id] = transcript

    # Updating the database with the fetched transcripts
    for video_id, transcript in transcripts_dict.items():
        update_video_transcript(connection, video_id, transcript)
