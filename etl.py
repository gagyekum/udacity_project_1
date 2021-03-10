import os
import glob
import psycopg2
import pandas as pd
from sql_queries import *


def process_song_file(cur, filepath):
    """Reads the song JSON data file and extract and load the needed columns for the song and 
    artist tables.
    :param cur: Database cursor for execution of database queries
    :param filepath: File path of the song JSON data file 
    """
    # open song file
    df = pd.read_json(filepath, lines=True)

    # get only needed columns
    df_song = df[["song_id", "title", "artist_id", "year", "duration"]]
    df_artist = df[["artist_id", "artist_name", "artist_location", "artist_latitude", "artist_longitude"]]

    # insert song record
    song_data = list(df_song.values[0])
    cur.execute(song_table_insert, song_data)
    
    # insert artist record
    artist_data = list(df_artist.values[0])
    cur.execute(artist_table_insert, artist_data)


def process_log_file(cur, filepath):
    """Reads the log JSON data file and extract data from the log JSON data file, 
    filter data extracted by the NextSong action, 
    does a convertion of the timestamp 
    column to human readable date and time, 
    extracts user details and song play data 
    then load data into the time, user and songplay tables
    :param cur: Database cursor for execution of database queries
    :param filepath: File path of the log JSON data file 
    """
    # open log file
    df = pd.read_json(filepath, lines=True)

    # filter by NextSong action
    df = df[df["page"] == "NextSong"]

    # convert timestamp column to datetime
    df["ts"] = pd.to_datetime(df["ts"], unit="ms")
    t = df
    
    # derive new dataframe using ts column
    time_data = (df["ts"], df["ts"].dt.hour, df["ts"].dt.day, df["ts"].dt.weekofyear,
                 df["ts"].dt.month, df["ts"].dt.year, df["ts"].dt.dayofweek)
    column_labels = ("start_time", "hour", "day", "week", "month", "year", "weekday")
    
    time_data_with_colums = list(zip(column_labels, time_data))
    time_data_dict = {column_label: time_data_value for column_label, time_data_value in time_data_with_colums}
    
    time_df = pd.DataFrame(time_data_dict, columns=column_labels)

    # insert time data records
    for i, row in time_df.iterrows():
        cur.execute(time_table_insert, list(row))

    # load user table
    user_df = df[["userId", "firstName", "lastName", "gender", "level"]]

    # insert user records
    for i, row in user_df.iterrows():
        cur.execute(user_table_insert, row)

    # insert songplay records
    for index, row in df.iterrows():
        
        # get songid and artistid from song and artist tables
        cur.execute(song_select, (row.song, row.artist, row.length))
        results = cur.fetchone()
        
        if results:
            songid, artistid = results
        else:
            songid, artistid = None, None

        # insert songplay record
        songplay_data = (row.ts, row.userId, row.level, songid, artistid, row.sessionId, row.location, row.userAgent)
        cur.execute(songplay_table_insert, songplay_data)


def process_data(cur, conn, filepath, func):
    """Extracts, transforms and load data from JSON files into
    postgresql database.
    :param cur: Database cursor for execution of database queries
    :param con: Database connection for connectivity to postgresql database
    :param filepath: File path of the log JSON data file 
    :param func: Function to process JSON files and load into postgresql database 
    """
    # get all files matching extension from directory
    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root,'*.json'))
        for f in files :
            all_files.append(os.path.abspath(f))

    # get total number of files found
    num_files = len(all_files)
    print('{} files found in {}'.format(num_files, filepath))

    # iterate over files and process
    for i, datafile in enumerate(all_files, 1):
        func(cur, datafile)
        conn.commit()
        print('{}/{} files processed.'.format(i, num_files))


def main():
    conn = psycopg2.connect("host=127.0.0.1 dbname=sparkifydb user=student password=student")
    cur = conn.cursor()

    process_data(cur, conn, filepath='data/song_data', func=process_song_file)
    process_data(cur, conn, filepath='data/log_data', func=process_log_file)

    conn.close()


if __name__ == "__main__":
    main()
