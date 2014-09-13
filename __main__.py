import databasetools.sqllib
import bin
# import scraper.Classes


if __name__ == '__main__':

    # Parameters for checking song_db
    db = databasetools.sqllib.song_db('BPMdatabase', 'bpmdatabase.db')

    table_name = 'my_songs'

    # drop table_name if it exists (to check if it works)
    db.drop_table(table_name)
    db.create_table(table_name)

    my_song_data = ['Radiohead', 'Time of my life', 'The Very Best of Neil Young', 9001, 'Electronic', 'Spam Recording Inc', 2015, 'H#']

    my_song = bin.music.Song(my_song_data)

    db.insert_song(my_song, table_name)
    print db.fetch_artist(my_song.artist, table_name)
