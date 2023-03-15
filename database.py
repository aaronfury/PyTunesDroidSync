import sqlite3 as sql

class SyncDB:
    def __init__(self,name) -> None:
        super().__init__(label=name)
        self.conn = None
        self.create_tables()

    def connect_db(self, file=':memory:'):
        try:
            self.conn = sql.connect(file)
        except sql.Error as e:
            print(e)

    def execute_db_command(self, command):
        try:
            c = self.conn.cursor()
            c.execute(command)
        except sql.Error as e:
            print(e)

    def create_tables(self):
        self.conn = self.connect_db('pytunes.db')

        sql_create_tracks_table = """ CREATE TABLE IF NOT EXISTS tracks (
                                            id integer PRIMARY KEY,
                                            title text NOT NULL,
                                            artist text NOT NULL,
                                            album text NOT NULL,
                                            filepath text NOT NULL UNIQUE,
                                            devicepath text UNIQUE
                                        ); """

        sql_create_playlists_table = """ CREATE TABLE IF NOT EXISTS playlists (
                                            id integer PRIMARY KEY,
                                            name text NOT NULL,
                                            FOREIGN KEY (tracks) REFERENCES trackid (id)
                                        );"""
        
        for command in (sql_create_tracks_table, sql_create_playlists_table):
            self.execute_db_command(command)

    def populate_playlists(self, playlist):
        print(f'Now loading {len(playlist.tracks)} tracks from {playlist.name} into database')

        # Loop through playlist.tracks
            # Try to match against existing file on device (use 95%+ string comparison of path, for things like encoding substitutions, etc)
        sql_insert_track = """
            INSERT OR IGNORE INTO tracks (title, artist, album, filepath, devicepath)
            VALUES ({title}, {artist}, {album}, {filepath})
        ;"""

    def populate_device(self, media):
        pass

    def get_device_adds(self):
        pass
    
    def get_device_deletions(self):
        pass