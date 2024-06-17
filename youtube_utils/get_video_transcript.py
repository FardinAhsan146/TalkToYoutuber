import os
import sys
from youtube_transcript_api import YouTubeTranscriptApi

def get_video_transcript(video_id: str) -> str:
    """
    Get the transcript of a YouTube video given its video_id. 
    Will clean it up and turn it into a document here. 
    The api doesn't return any other USEFUL information.
    """
    transcript = YouTubeTranscriptApi.get_transcript(video_id)
    text = ' '.join([line['text'] for line in transcript])
    return text 
