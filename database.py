import sqlite3 as sql

conn = None

def connect_db(file=':memory:'):
    global conn
    try:
        conn = sql.connect(file)
    except sql.Error as e:
        print(e)
    finally:
        return conn

def execute_db_command(command):
    global conn
    try:
        c = conn.cursor()
        c.execute(command)
    except sql.Error as e:
        print(e)

if __name__ == '__main__':
    conn = connect_db('pytunes.db')

    sql_create_localtracks_table = """ CREATE TABLE IF NOT EXISTS localtracks (
                                        id integer PRIMARY KEY,
                                        title text NOT NULL,
                                        filepath text,
                                    ); """

    sql_create_devicetracks_table = """CREATE TABLE IF NOT EXISTS devicetracks (
                                    id integer PRIMARY KEY,
                                    title text NOT NULL,
                                    filepath text
                                    FOREIGN KEY (localtrack) REFERENCES localtracks (id)
                                );"""
    
    for command in (sql_create_localtracks_table,sql_create_devicetracks_table):
        execute_db_command(command)