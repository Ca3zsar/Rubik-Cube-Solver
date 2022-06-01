import sqlite3
con = sqlite3.connect('corners.db', isolation_level=None)

cursor = con.cursor()

def create_table():
    cursor.execute('''CREATE TABLE IF NOT EXISTS corners
                   (config BLOB UNIQUE, moves BLOB)''')

    con.commit()


def add_row(config, moves):
    config = sqlite3.Binary(config)
    moves = sqlite3.Binary(moves)
    try:
        cursor.execute('''INSERT INTO corners VALUES (?,?)''', (config, moves))
    except sqlite3.IntegrityError:
        pass

def close_connection():
    con.close()