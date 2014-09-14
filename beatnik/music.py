"""
This file contains the music classes for the BeatNik project.
Please see BeatNik/documentation.txt for further information
regarding this file (nothing yet).

Newest Changes:
    -Created file. -J 9/12/14
"""

class Song(object):
    'Song Class is for formatting and maintaining song data.'

    def __init__(self, song_data):

        self.data  = song_data
        self.refresh(song_data)

    def refresh(self, data):
        'Method for assigning and renewing data. Allows data editing to'
        'be done solely with self.data.'

        """
        Song.data order will be:
        [artist, title, album, BPM, genre, label, year, key]
        """
        self.data   = data
        self.artist = self.data[0]
        self.title  = self.data[1]
        self.album  = self.data[2]
        self.BPM    = self.data[3]
        self.genre  = self.data[4]
        self.label  = self.data[5]
        self.year   = self.data[6]
        self.key    = self.data[7]


    def change_to(self, index, new_value):
        'Method for changing song data.'
        try:
            self.data[index] = new_value
        except Exception as e:
            raise IndexError('Index must be value 0-%s.' % len(self.data))
        return self.refresh()


    def __add__(self, other):
        'Method for merging songs together. data[i] must be identical'
        'or one \'Null\' to merge.'
        'Type: Song -> Song -> Song'
        merged_song_data = []

        if self.__ne__(other):
            raise Exception('Songs must have same attributes or be \'Null\'')

        for i, element in enumerate(self.data):
            if element == '':
                merged_song_data.append(element)
            else:
                merged_song_data.append(other.data[i])

        return Song(merged_song_data)

    #Comparison Methods
    def __eq__(self, other):
        'Method for determining equality of songs.'
        'Type: Song -> Song -> Bool'
        #Requires at least song and artist to be equal
        if self.data[:2] != other.data[:2]:
            return False
        for i, element in enumerate(self.data):
            if element != other.data[i] and '' not in [element, other.data[i]]:
                return False
        return True


    def __ne__(self, other):
        return not self.__eq__(other)


    def __nonzero__(self):  #Runs when bool(Song) is called eg. if Song():
        if self.data[:2] == ['', '']:
            return True
        return False


    def __str__(self):  #Runs when str(Song) is called eg. print Song(x).
        rep_0 = "This is %s by %s, played at %s in the key of %s.\n" % (
                            self.title, self.artist, self.BPM, self.key)
        rep_1 = "It is from the album %s, produced by %s in %s."     % (
                                      self.album, self.label, self.year)
        return rep_0 + rep_1


    def __repr__(self):
        return repr(self.data)
