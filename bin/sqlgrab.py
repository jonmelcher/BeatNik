import sqlite3

conn = sqlite3.connect('bpmdatabase.db')
c = conn.cursor()

# the documentation recommends this syntax.
t = ('Radiohead', )
c.execute('SELECT * FROM songs WHERE artist=?', t)
print c.fetchone()
