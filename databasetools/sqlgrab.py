import sqlite3

conn = sqlite3.connect('bpmdatabase.db')
c = conn.cursor()

t = ('Radiohead', )
c.execute('SELECT * FROM songs WHERE artist=?', t)
print c.fetchone()
