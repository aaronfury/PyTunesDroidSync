import sqlite3 as sql

class SyncDB(object):
    def __init__(self, file=':memory:'):
        print(f'Connecting to sqlite database {file}')
        self.conn = sql.connect(file)
        self.cursor = self.conn.cursor()
    
    def close(self):
        self.conn.close()

    def create_tables(self):
        sql_create_tracks_table = """
            CREATE TABLE IF NOT EXISTS tracks (
            id integer PRIMARY KEY,
            title text NOT NULL,
            artist text NOT NULL,
            album text NOT NULL,
            filepath text NOT NULL UNIQUE,
            devicepath text UNIQUE
            );
        """
        
        self.cursor.execute(sql_create_tracks_table)

    def populate_playlist(self, playlist):
        print(f'Now loading {len(playlist.tracks)} tracks from {playlist.name} into database')

        sql_create_playlist_table = f"""
            CREATE TABLE IF NOT EXISTS pl_{playlist.name} (
                id integer PRIMARY KEY,
                trackid integer REFERENCES tracks(id),
                pl_order integer UNIQUE
            );
        """
        self.cursor.execute(sql_create_playlist_table)

        for track in playlist.tracks:
            sql_insert_track = f"""
                INSERT OR IGNORE INTO tracks (title, artist, album, filepath)
                VALUES (?, ?, ?, ?)
                RETURNING id
                ;
            """

            self.cursor.execute(sql_insert_track, (track.name, track.artist, track.album, track.location))

            sql_insert_pl_entry = f"""
                INSERT OR IGNORE INTO pl_{playlist.name} (trackid, pl_order)
                VALUES (?, ?)
                ;
            """

            self.cursor.execute(sql_insert_pl_entry, (next(self.cursor), track.playlist_order))

        print(f'Done.')

    def populate_device(self, media):
        pass

    def get_device_adds(self):
        pass
    
    def get_device_deletions(self):
        pass