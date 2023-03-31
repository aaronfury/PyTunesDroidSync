import sqlite3 as sql

class SyncDB(object):
    def __init__(self, file=':memory:'):
        print(f'Connecting to sqlite database {file}')
        self.conn = sql.connect(file)
        self.cursor = self.conn.cursor()

        self.sql_create_tracks_table = """
            CREATE TABLE IF NOT EXISTS tracks (
            id integer PRIMARY KEY,
            title text NOT NULL,
            artist text NOT NULL,
            album text NOT NULL,
            filepath text NOT NULL UNIQUE,
            devicepath text UNIQUE
            );
        """
        self.sql_create_playlist_table = """
            CREATE TABLE IF NOT EXISTS "pl_{}" (
                id integer PRIMARY KEY,
                trackid integer REFERENCES tracks(id),
                pl_order integer UNIQUE
            );
        """
        self.sql_insert_pl_tracks = """
            INSERT OR IGNORE INTO tracks (title, artist, album, filepath)
            VALUES (?, ?, ?, ?)
            ;
        """
        self.sql_insert_track = """
            INSERT OR IGNORE INTO tracks (title, artist, album, filepath)
            VALUES (?, ?, ?, ?)
            ;
        """
        self.sql_select_track = """
            SELECT id FROM tracks
            WHERE filepath = "{}"
        """
        self.sql_insert_pl_entry = """
            INSERT OR IGNORE INTO "pl_{}" (trackid, pl_order)
            VALUES (?, ?)
            ;
        """
    
    def close(self):
        self.conn.close()

    def create_tables(self):        
        self.cursor.execute(self.sql_create_tracks_table)

    def populate_playlist(self, playlist):
        print(f'Now loading {len(playlist.tracks)} tracks from {playlist.name} into database')

        sql_create_pl_table = self.sql_create_playlist_table.format(playlist.name)
        self.cursor.execute(sql_create_pl_table)
        
        # Create an iterable list of values for the tracks, so we can do bulk operations directly
        # TODO: BETTER WAY TO DO THIS WITHOUT THE FOR LOOP?
        tracks = []
        for track in playlist.tracks:
            tracks.append((track.name, track.artist, track.album, track.location))

        self.cursor.executemany(self.sql_insert_pl_tracks, tracks)
        
        for track in playlist.tracks:           
            for row in self.cursor.execute(self.sql_select_track.format(track.location)):
                self.cursor.execute(self.sql_insert_pl_entry.format(playlist.name), (row[0], track.playlist_order))

        self.conn.commit()
        print('Done.')

    def populate_device(self, media):
        pass

    def get_device_adds(self):
        pass
    
    def get_device_deletions(self):
        pass