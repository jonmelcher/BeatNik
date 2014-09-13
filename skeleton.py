ass SongFinder(object):
    'SongFinder class searches for song data to add to SQL database.'
    
    def fetch_song_data(songname):
        return [artist, album, songname, bpm]

    def song_crawler():
        for page in website:
            songs = crawl_for_songname(page)
  
        for song in songs:
            database.add(fetch_song_data(song))

class Playlist(object):
  'A user\'s playlist.'
  
  def __init__(name, owner, songs=[]): 
    self.name = name
    self.owner = owner
    self.songs = songs """ songs = [order,[songdata]]"""
    self.order = None
    # initializing a playlist should not add any songs? maybe as an option
    # you either have them at the start or add them in later, up to you
    
  def search(self, song):
    return None
  
  def add(self, song):
    return None

  def remove(self, song):
    return None
  
  def clear(self):
    self.songs = []
  
  def randomize():
    return None
 
class Song(object):
  'A song.'
  
  def __init__(data):
    self.title = data[0]
    # etc
  
  def edit_title():
    return None
  
  def edit_artist():
    return None  

  def edit_etc():
    return None
  
  
class SongDatabase(object):
    'SongDatabase class ties in GUI with SQL database'

    def search(song/artist/etc)
        'Searches for a single song and displays information'
    


# move this to the Playlist class?


    # I think those details can be figured out later. We can get a skeleton written 
    # and start with the goal of being able to parse a hard-coded web-page and add 
    # it to the databse
