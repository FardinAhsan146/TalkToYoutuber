import scrapetube
from typing import List
from tqdm import tqdm
from sqlite3 import Connection
import os
import sys

# Add the parent directory to the sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
sys.path.append(parent_dir)

from database.database_utils import insert_initial_row, create_connection, video_exists

def get_videos(channel_name: str, connection : Connection) -> List[str]:
    """
    Refer to documentation for main fetch method: https://scrapetube.readthedocs.io/en/latest/
    Honestly, keeping the generator in memory is not feasible for channels that have a large number of videos.
    We should just write into the sqlite table. Its easy to query from the CLI anyways.
    """
    videos = scrapetube.get_channel(channel_username = channel_name)
    for video in tqdm(videos, desc = f"Fetching videos for channel '{channel_name}'"):
        video_id = video['videoId'] # https://www.youtube.com/watch?v=<video_id>
        if video_exists(connection, video_id):
            continue
        video_title = video['title']['runs'][0]['text']
        # Insert the video_id into the database
        insert_initial_row(connection, channel_name, video_id, video_title)

    shorts = scrapetube.get_channel(channel_username = channel_name, content_type = 'shorts')
    for short in tqdm(shorts, desc = f"Fetching shorts for channel '{channel_name}'"):
        video_id = short['videoId']
        if video_exists(connection, video_id):
            continue
        video_title = short['headline']['simpleText']
        # Insert the video_id into the database
        insert_initial_row(connection, channel_name, video_id, video_title)

    
