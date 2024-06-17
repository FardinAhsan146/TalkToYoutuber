import os
import sys
from typing import List
from tqdm import tqdm
from youtube_transcript_api import YouTubeTranscriptApi

# Add the parent directory to the sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
sys.path.append(parent_dir)

from sqlite.database_utils import update_video_transcript, create_connection
connection = create_connection()

def get_video_transcript(video_id: str) -> str:
    """
    Get the transcript of a YouTube video given its video_id. 
    Will clean it up and turn it into a document here. 
    The api doesn't return any other USEFUL information.
    """
    transcript = YouTubeTranscriptApi.get_transcript(video_id)
    text = ' '.join([line['text'] for line in transcript])
    return text 
