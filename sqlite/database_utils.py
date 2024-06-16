import sqlite3
from sqlite3 import Connection
from typing import Optional

def create_connection(db_name: str) -> Optional[Connection]:
    """Create a database connection to the SQLite database specified by db_name."""
    conn: Optional[Connection] = None
    try:
        conn = sqlite3.connect(db_name)
        print(f"Connected to database '{db_name}'")
    except sqlite3.Error as e:
        print(e)
    return conn

def create_table(conn: Connection) -> None:
    """Create a table named video_contents with three string fields."""
    create_table_sql = '''
    CREATE TABLE IF NOT EXISTS video_contents (
        channel_name TEXT NOT NULL,
        video_id TEXT NOT NULL,
        video_transcript TEXT
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

def insert_into_table(conn: Connection, channel_name: str, video_id: str, video_transcript: str) -> None:
    """Insert a new row into the video_contents table only if the video_id doesn't already exist."""
    check_sql = '''
    SELECT 1 FROM video_contents WHERE video_id = ? LIMIT 1;
    '''
    insert_sql = '''
    INSERT INTO video_contents (channel_name, video_id, video_transcript)
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
            cursor.execute(insert_sql, (channel_name, video_id, video_transcript))
            conn.commit()
            print("New row inserted into 'video_contents'.")
    except sqlite3.Error as e:
        print(e)


if __name__ == '__main__':
    # db_name: str = 'sqlite/talk_to_youtuber_db.sqlite'

    # # Create a database connection
    # conn: Optional[Connection] = create_connection(db_name)

    # if conn:
    #     # Create the video_contents table
    #     create_table(conn)

    #     # Insert a test row
    #     insert_into_table(conn, 'MyChannel', '12345', 'This is a test transcript.')

    #     # Delete the video_contents table
    #     #delete_table(conn)

    #     # Close the database connection
    #     conn.close()
    pass  