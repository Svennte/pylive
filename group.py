from live.object import *

class Group (LoggingObject):
	""" Represents a grouped set of Track objects.
	Because we can't programmatically query whether a track in Live is an
	individual or group track, the user must name groups using a special
	format which is passed to set.scan(group_re = RE)

	Properties:
	track_index -- The numerical track index of this group
	group_index -- Groups are auto-numbered from 0
	name -- Human-readable name
	tracks -- List of Track objects contained within this group
	"""

	def __init__(self, set, track_index, group_index, name):
		self.set = set
		self.track_index = track_index
		self.group_index = group_index
		self.indent = 1
		self.name = name
		self.tracks = []

	def __str__(self):
		string = "live.group(%d): %s" % (self.group_index, self.name)
		if len(self.tracks):
			string = string + " [tracks %d-%d]" % (self.tracks[0].index, self.tracks[len(self.tracks) - 1].index)
		return string

	def add_track(self, track):
		""" Append a new track to this group. Should probably only be called by Set.scan(). """
		self.tracks.append(track)

	def dump(self):
		self.trace("%d tracks" % len(self.tracks))
		for track in self.tracks:
			track.dump()