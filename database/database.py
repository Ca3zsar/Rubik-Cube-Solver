import sqlite3
con = sqlite3.connect('corners.db')

cursor = con.cursor()

# Create table
cursor.execute('''CREATE TABLE IF NOT EXISTS corners
               (config BLOB, moves BLOB)''')

con.commit()

con.close()