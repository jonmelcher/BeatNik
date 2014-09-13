import beatnik.sqllib
import beatnik.music
import beatnik.scrapers

# import scraper.Classes


if __name__ == '__main__':

    # Parameters for checking song_db
    db = beatnik.sqllib.song_db('BPMdatabase 0 to 9', 'databases/0-to-9.db')

    table_name = 'numeric_songs'

    # drop table_name if it exists (to check if it works)
    db.drop_table(table_name)
    db.create_song_table(table_name)

    scraper = beatnik.scrapers.BPMDB()

    # only scrape band-names starting with '1' or '2'
    songs = scraper.scrape('12')

    print 'scraped'

    for song in songs:

        problem = False
        for s in song.data:

            # we need to take care of escape characters, as they don't
            # play well with sqlite3
            if s.find('\'') != -1:
                # print 'data = %s' % song.data
                # print 'artist = %s' % song.artist
                # print 'title = %s' % song.title
                # print 'album = %s' % song.album
                # print 'BPM = %s' % song.BPM
                # print 'genre = %s' % song.genre
                # print 'label = %s' % song.label
                # print 'year = %s' % song.year
                # print 'key = %s' % song.key
                problem = True
        if not problem:
            db.insert_song(song, table_name)

    print 'done with insertions'

    # db.cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    # print(db.cursor.fetchall())

    # t = ('Radiohead', )
    # db.cursor.execute('SELECT * FROM my_songs WHERE artist=?', t)

    print db.fetch_artist('Radiohead', table_name)
    print db.fetch_artist('2 Pac', table_name)

    artist = '2 Pac'
    t = (artist, )
    db.cursor.execute('SELECT * FROM %s WHERE artist=?' % table_name, t)
    print db.cursor.fetchall()

    contents = db.table_contents(table_name)
    for song in contents:
        print song
