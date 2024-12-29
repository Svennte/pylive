
import sys
print(sys.path)
#------------------------------------------------------------------------
# Basic example of pylive usage: connect to the Live set, trigger a clip,
# and modulate some device parameters.
#------------------------------------------------------------------------
import live
import random

#------------------------------------------------------------------------
# Query the set's contents, and set its tempo to 110bpm.
#------------------------------------------------------------------------
set = live.Set(scan=True)
set.tempo = 110.0

#------------------------------------------------------------------------
# Each Set contains a list of Track objects.
#------------------------------------------------------------------------
track = set.tracks[0]
print("Track name '%s'" % track.name)

#------------------------------------------------------------------------
# Each Track contains a list of Clip objects.
#------------------------------------------------------------------------
clip = track.clips[0]
print("Clip name '%s', length %d beats" % (clip.name, clip.length))