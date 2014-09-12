'''
An example of how to add to a database.
'''

import sqlite3

# connect to a database
conn = sqlite3.connect('bpmdatabase.db')

# cursors let you do things. don't ask me why
c = conn.cursor()

# Set to true to initialize the table
create_new_table = False
if create_new_table:
    Create a table
    c.execute('''CREATE TABLE songs
                (title text, artist text, album text, label text, year int, genre text, BPM real)''')

c.execute('''INSERT INTO songs VALUES
             ('Fake Plastic Trees', 'Radiohead', 'NULL', 74, 'NULL', 'Capitol Records', 1995)''')

conn.commit()

# make sure to close cursors
c.close()
