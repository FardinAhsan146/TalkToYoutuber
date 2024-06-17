import os
import sys
import youtube_transcript_api 

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

