import os
import glob
import psycopg2
import pandas as pd
from sql_queries import *


def process_song_file(cur, filepath):
    """
    Processes files in json format from the song dataset by inserting data from relevant columns into songs and artists table.

    Parameters:
            cur(obj): Cursor object of database where processed file contents are to be stored.
            filepath(str): filepath to a single song file.
    """
    # open song file
    df = pd.read_json(filepath, lines=True)

    # insert song record
    song_data = df[['song_id','title', 'artist_id', 'year', 'duration']].values.tolist()[0]
    try:
        cur.execute(song_table_insert, song_data)
    except psycopg2.Error as e:
        print("Error: Inserting Song Data")
        print (e)

    # insert artist record
    artist_data = df[['artist_id', 'artist_name', 'artist_location', 'artist_latitude', 'artist_longitude']].values.tolist()[0]
    try:
        cur.execute(artist_table_insert, artist_data)
    except psycopg2.Error as e:
        print("Error: Inserting Artist Data")
        print (e)


def process_log_file(cur, filepath):
    """
    Processes log files in json format from the log dataset by inserting data from relevant columns into time, users and songplays table.

    Parameters:
            cur(obj): Cursor object of database where processed file contents are to be stored.
            filepath(str): filepath to a single log file.
    """
    # open log file
    df = pd.read_json(filepath, lines=True)

    # filter by NextSong action
    df = df[df['page']=='NextSong']

    # convert timestamp column to datetime
    t = pd.to_datetime(df.ts, unit='ms')

    # insert time data records
    time_data = [t.values, t.dt.hour, t.dt.day, t.dt.week, t.dt.month, t.dt.year, t.dt.weekday < 5]
    column_labels = ['Timestamp', 'Hour', 'Day', 'Week of Year', 'Month', 'Year', 'Weekday']
    time_df = pd.DataFrame({column_labels[i]: time_data[i] for i in range(len(column_labels))})

    for i, row in time_df.iterrows():
        try:
            cur.execute(time_table_insert, list(row))
        except psycopg2.Error as e:
            print("Error: Inserting Time Data")
            print (e)

    # load user table
    user_df = df[['userId','firstName', 'lastName', 'gender', 'level']]

    # insert user records
    for i, row in user_df.iterrows():
        try:
            cur.execute(user_table_insert, row)
        except psycopg2.Error as e:
            print("Error: Inserting User Data")
            print (e)

    # insert songplay records
    for index, row in df.iterrows():

        # get songid and artistid from song and artist tables
        try:
            cur.execute(song_select, (row.song, row.artist, row.length))
        except psycopg2.Error as e:
            print("Error: Selecting Song Id and Artist Id Data")
            print (e)
        results = cur.fetchone()

#         if results is not None: #added to check insert into songplay table
#             print(results)

        if results:
            songid, artistid = results
        else:
            songid, artistid = None, None

        # insert songplay record
        songplay_data = (pd.to_datetime(row.ts, unit='ms'), row.userId, row.level, songid, artistid, row.sessionId, row.location,row.userAgent)
        try:
            cur.execute(songplay_table_insert, songplay_data)
        except psycopg2.Error as e:
            print("Error: Inserting Song Play Data")
            print (e)


def process_data(cur, conn, filepath, func):
    """
    Parses a list of filepaths into appropriate format, calls a function to process files in the all filepaths and documents the progress with processing.

    Parameters:
            cur(obj): Cursor object of database where processed file contents are to be stored.
            conn(obj): Connection object of database where processed file contents are to be stored.
            filepath(str): Directory to a collection of files to be processed.
            func(Obj): Object of the function for processing the file contents.
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
        print('{}/{} files processed.'.format(i, num_files))


def main():
    try:
        conn = psycopg2.connect("host=127.0.0.1 dbname=sparkifydb user=student password=student")
    except psycopg2.Error as e:
        print("Error: Could not make connection to the Postgres database")
        print(e)

    try:
        cur = conn.cursor()
    except psycopg2.Error as e:
        print("Error: Could not get cursor to the Database")
        print(e)

    conn.set_session(autocommit=True)

    process_data(cur, conn, filepath='data/song_data', func=process_song_file)
    process_data(cur, conn, filepath='data/log_data', func=process_log_file)

    cur.close()
    conn.close()


if __name__ == "__main__":
    main()
