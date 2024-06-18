import sqlite3
from sqlite3 import Connection
from typing import Optional

def create_connection(db_name: str = 'talk_to_youtuber_db.sqlite') -> Optional[Connection]:
    """Create a database connection to the SQLite database specified by db_name."""
    conn: Optional[Connection] = None
    try:
        conn = sqlite3.connect(db_name)
        print(f"Connected to database '{db_name}'")
    except sqlite3.Error as e:
        print(e)
    return conn

def create_table(conn: Connection) -> None:
    """Create a table named video_contents with four string fields."""
    create_table_sql = '''
    CREATE TABLE IF NOT EXISTS video_contents (
        channel_name TEXT NOT NULL,
        video_id TEXT NOT NULL,
        video_title TEXT,
        video_transcript TEXT,
        transcript_attempted BOOLEAN DEFAULT FALSE
    );
    '''
    try:
        cursor = conn.cursor()
        cursor.execute(create_table_sql)
        conn.commit()
        print("Table 'video_contents' created.")
    except sqlite3.Error as e:
        print(e)

def delete_table(conn: Connection) -> None:
    """Delete the video_contents table if it exists."""
    delete_table_sql = 'DROP TABLE IF EXISTS video_contents;'
    try:
        cursor = conn.cursor()
        cursor.execute(delete_table_sql)
        conn.commit()
        print("Table 'video_contents' deleted.")
    except sqlite3.Error as e:
        print(e)

def insert_initial_row(conn: Connection, channel_name: str, video_id: str, video_title: str) -> None:
    """Insert a new row into the video_contents table with channel_name, video_id, and video_title only if the video_id doesn't already exist."""
    check_sql = '''
    SELECT 1 FROM video_contents WHERE video_id = ? LIMIT 1;
    '''
    insert_sql = '''
    INSERT INTO video_contents (channel_name, video_id, video_title)
    VALUES (?, ?, ?);
    '''
    try:
        cursor = conn.cursor()
        
        # Check if the video_id already exists
        cursor.execute(check_sql, (video_id,))
        exists = cursor.fetchone()
        
        if exists:
            print(f"Video ID '{video_id}' already exists. No new row inserted.")
        else:
            # Proceed with insertion
            cursor.execute(insert_sql, (channel_name, video_id, video_title))
            conn.commit()
    except sqlite3.Error as e:
        print(e)

def update_video_transcript(conn: Connection, video_id: str, video_transcript: str) -> None:
    """Update the video_transcript of the row that matches the given video_id."""
    from sqlite3 import Error
    update_sql = '''
    UPDATE video_contents 
    SET video_transcript = ?, transcript_attempted = TRUE
    WHERE video_id = ?;

    TODO: ADD ATTEMPTED TRANSCRIPT field 
    '''
    try:
        cursor = conn.cursor()

        # Check if the video_id exists and if a transcript already exists
        cursor.execute('SELECT video_transcript FROM video_contents WHERE video_id = ? LIMIT 1;', (video_id,))
        result = cursor.fetchone()
        
        if result:
            existing_transcript = result[0]
            if existing_transcript is not None:
                return
            
            # Proceed with the update as no transcript exists
            cursor.execute(update_sql, (video_transcript, video_id))
            conn.commit()
        else:
            print(f"Video ID '{video_id}' does not exist. No update made.")
    except Error as e:
        print(e)

def check_transcript_attempted(conn: Connection, video_id: str) -> bool:
    """Check if transcript was attempted for a given video_id."""
    check_sql = '''
    SELECT transcript_attempted FROM video_contents WHERE video_id = ?;
    '''
    try:
        cursor = conn.cursor()
        cursor.execute(check_sql, (video_id,))
        row = cursor.fetchone()
        if row:
            return row[0] == 1  # Check for True (BOOLEAN)
        return False
    except sqlite3.Error as e:
        print(e)
        return False

def reset_transcript_attempted(conn: Connection, video_id: str) -> None:
    """Reset the transcript_attempted to False for a given video_id."""
    update_sql = '''
    UPDATE video_contents 
    SET transcript_attempted = FALSE 
    WHERE video_id = ?;
    '''
    try:
        cursor = conn.cursor()
        cursor.execute(update_sql, (video_id,))
        conn.commit()
    except sqlite3.Error as e:
        print(e)

def get_videos_by_channel(conn: Connection, channel_name: str) -> Optional[list]:
    """Get all video content for a given channel name."""
    select_sql = '''
    SELECT * FROM video_contents WHERE channel_name = ?;
    '''
    try:
        cursor = conn.cursor()
        cursor.execute(select_sql, (channel_name,))
        rows = cursor.fetchall()

        if rows:
            return rows
        else:
            print(f"No videos found for channel '{channel_name}'.")
            return None
    except sqlite3.Error as e:
        print(e)
        return None

if __name__ == '__main__':
    # db_name: str = 'talk_to_youtuber_db.sqlite'

    # # Create a database connection
    # conn: Optional[Connection] = create_connection(db_name = db_name )

    # if conn:
    #     #Create the video_contents table
    #     create_table(conn)

    #     # Insert a test row
    #     insert_initial_row(conn, 'MyChannel', '12345', 'This is a test title.')

    #     # Update video transcript
    #     update_video_transcript(conn, '12345', 'This is a test transcript.')

    #     # Delete the video_contents table
    #     delete_table(conn)

    #     # Close the database connection
    #     conn.close()
    pass 

