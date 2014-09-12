import sqlite3
conn = sqlite3.connect('bpmdatabase.db')

c = conn.cursor()

# Create a table
# c.execute('''CREATE TABLE songs
#              (title text, artist text, album text, label text, year int, genre text, BPM real)''')

c.execute('''INSERT INTO songs VALUES
             ('Fake Plastic Trees', 'Radiohead', 'NULL', 74, 'NULL', 'Capitol Records', 1995)''')

c.execute('''DELETE FROM songs
             WHERE title='Radiohead' ''')

conn.commit()

c.close()
