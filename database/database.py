import sqlite3
con = sqlite3.connect('corners.db')

cursor = con.cursor()


def create_table():
    cursor.execute('''CREATE TABLE IF NOT EXISTS corners
                   (config BLOB, moves BLOB)''')

    con.commit()


def add_row(config, moves):
    config = sqlite3.Binary(config)
    moves = sqlite3.Binary(moves)
    cursor.execute('''INSERT INTO corners VALUES (?,?)''', (config, moves))

    con.commit()


def close_connection():
    con.close()