import beatnik.sqllib
import beatnik.music
# import scraper.Classes


if __name__ == '__main__':

    # Parameters for checking song_db
    db = beatnik.sqllib.song_db('Sample BPM DB', 'databases/sample.db')

    table_name = 'my_songs'

    # drop table_name if it exists (to check if it works)
    db.drop_table(table_name)
    db.create_song_table(table_name)

    my_song_data = ["-1", '1', '1', 1, 'Acid Techno', '1', 1, 'NULL']
    my_song_data = ["-1", '1', '1', 1, 'Acid Techno', '1', 1, 'NULL']


    my_song = beatnik.music.Song(my_song_data)

    db.insert_song(my_song, table_name)

    print db.fetch_artist(my_song.artist, table_name)
    # print db.fetch_artist('radioHead', table_name)

