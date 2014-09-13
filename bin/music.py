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

        self.data     = song_data
        self.artist   = None
        self.title    = None
        self.album    = None
        self.BPM      = None
        self.genre    = None
        self.label    = None
        self.year     = None
        self.key      = None


    def refresh(self):
        'Method for assigning and renewing data. Allows data editing to'
        'be done solely with self.data.'
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
            raise IndexError('Index must be values 0-%s' % len(self.data))
        return self.refresh()


    def __add__(self, other):
        'Method for merging songs together. data[i] must be identical'
        'or one \'Null\' to merge.'
        'Type: Song -> Song -> Song'
        merged_song_data = []
        for i, element in enumerate(self.data):
            if element == other.data[i]:
                merged_song_data.append(element)
            elif element == 'Null':
                merged_song_data.append(other.data[i])
            elif other.data[i] == 'Null':
                merged_song_data.append(element)
            else:
                raise ValueError('.data must match other than Null values.')

        return Song(merged_song_data)


    def __eq__(self, other):
        'Method for determining equality of songs.'
        'Type: Song -> Song -> Bool'
        if self.data[:2] == other.data[:2]:
            return True
        return False


    def __ne__(self, other):
        return not self.__eq__(other)


    def __repr__(self):
        return repr(self.data)
