"""
This file contains the classes for the BeatNik project.

Newest Changes:
	-Created file - J 9/9/14
"""

class Song(object):
	'Song Class is for formatting and maintaining song data.'

	def __init__(self, song_data):

		self.data     = song_data
		self.artist   = song_data[0]
		self.title    = song_data[1]
		self.album    = song_data[2]
		self.BPM      = song_data[3]
		self.genre    = song_data[4]
		self.label    = song_data[5]
		self.year     = song_data[6]
		self.playlist = []


	def refresh(self):
		'Method for renewing data.'
		'Allows data editing to be'
		'Solely with self.data.'
		self.artist = self.data[0]
		self.title  = self.data[1]
		self.album  = self.data[2]
		self.BPM    = self.data[3]
		self.genre  = self.data[4]
		self.label  = self.data[5]
		self.year   = self.data[6]


	def changeTo(self, index, new_value):
		'Method for changing song data.'
		try:
			self.data[index] = new_value
		except Exception as e:
			raise IndexError('Index must be values 0-6.')
		return self.refresh()


	def __repr__(self):
		return repr(self.data)