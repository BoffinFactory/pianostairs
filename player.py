import config as G, pygame, itertools, collections, sys, os, gui

# Output functions.  Depending on the physical interface, I might want these doing different things
def output(s):
	G.gui.write(s)

def error(s):
	output("ERROR: " + s)

def debug(s):
	if G.DEBUG: output("DEBUG: " + s)

def get_sound_file(instrument, note):
	return G.SOUNDS_DIR + '/' + instrument + '-' + note + '.wav'

def sound_play(note):
	if not G.power: return

	fname = get_sound_file(G.instrument, note)
	channel = pygame.mixer.Channel(G.index_from_note[note])
	channel.play(pygame.mixer.Sound(fname))
	debug("start %s on channel %d\n" % (fname, G.index_from_note[note]))

def sound_stop(note):
	channel = pygame.mixer.Channel(G.index_from_note[note])
	channel.stop()
	debug("stop channel %d\n" % (G.index_from_note[note]))

def stair_down(stair_num):
	if not G.power: return
	sound_play(G.note_from_stair[stair_num])

def stair_up(stair_num):
	sound_play(G.note_from_stair[stair_num])

#key is the *major* key it's in.  It'll be centered on that note in octave 4
def set_key(key, include_accidentals):
	arr = [ 'C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab', 'A', 'Bb', 'B' ]

	if key not in arr:
		error("key %s is invalid.  Select one of %s" % (key, arr))
		return None

	offset = arr.index(key)
	notes = ["%s%d" % (note,octave) 
		for (i, (octave,note)) in enumerate(itertools.product(range(0, 9), arr)) 
		if include_accidentals or ((i - offset) % 12 not in [ 1, 3, 6, 8, 10 ]) # filter accidentals
	]

	# Center on octave 4
	center = notes.index(key + '4')
	min = center - G.NSTAIRS / 2

	# Reduce to G.NSTAIRS notes
	assert min >= 0 and len(notes) >= G.NSTAIRS
	G.note_from_stair = notes[min : G.NSTAIRS + min]
	assert len(G.note_from_stair) == G.NSTAIRS

def set_instrument(name):
	# We assume that the files were set up properly, so if C4 exists, the rest do as well
	fname = get_sound_file(name, 'C4')
	if not name in list_instruments():
		error("%s is not a valid instrument" % (name))
		return None

	G.instrument = name


# Should be possible to enable or disable the entire thing
def system_on():
	G.power = 1

def system_off():
	G.power = 0
	pygame.mixer.stop()

def play_song(fname):
	# easter egg: override the normal working and play a full song
	pass

def list_instruments():
	lst = list(set([ fname.split('-')[0] for fname in os.listdir(G.SOUNDS_DIR) ]))
	lst.sort()
	return lst

def init():
	pygame.mixer.pre_init(44100, -16, 2, 2048)
	pygame.mixer.init()
	pygame.mixer.set_num_channels(88)
	pygame.init()

	arr = [ 'C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab', 'A', 'Bb', 'B' ]
	allnotes = ["%s%d" % (note,octave) 
		for (i, (octave,note)) in enumerate(itertools.product(range(0, 9), arr)) 
	]
	allnotes = allnotes[allnotes.index('A0') : allnotes.index('C8') + 1]

	for i in range(0, len(allnotes)): G.index_from_note[allnotes[i]] = i

def cleanup():
	pygame.mixer.quit()

def test():
	init()

	for key in [ 'C', 'G', 'D', 'E', 'B', 'Gb', 'Db', 'Ab', 'Eb', 'Bb', 'F' ]:
		set_key(key, 0)
		sys.stdout.write("%2s: " % (key))
		print(set([ i[0:2] 
			for i in G.note_from_stair 
			if -1 != i.find('b') ]))

if '__main__' == __name__ :
	test()
