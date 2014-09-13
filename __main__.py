import databasetools.sqldump
import bin
# import scraper.Classes


if __name__ == '__main__':
    db = databasetools.sqldump.song_db('BPMdatabase', 'bpmdatabase.db')
    table_name = 'my_songs'
    db.drop_table(table_name)
    db.create_table(table_name)

    my_song_data = ['Radiohead', 'Time of my life', 'The Very Best of Neil Young', 9001, 'Electronic', 'Spam Recording Inc', 2015]

    my_song = bin.Classes.Song(my_song_data)


    db.insert_song(my_song, table_name)

    db.fetch_artist(my_song.artist, table_name)
