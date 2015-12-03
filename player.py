import pygame, itertools, collections, sys, os, gui

# Constants
NSTAIRS = 32
STEPS_PER_FLIGHT = 16
SOUNDS_DIR = 'sounds'
DEBUG = 0

# Globals. Don't modify these directly.  set_(key|instrument) and power_(on|off) run additional checks and/or do stuff.
g_instrument = 'piano'
g_note_from_stair = []
g_index_from_note = {}
g_power = 1 # if 0, nothing runs

# Output functions.  Depending on the physical interface, I might want these doing different things
def output(s):
	gui.extern_kludge().write(s)

def error(s):
	output("ERROR: " + s)

def debug(s):
	global DEBUG
	if DEBUG: output("DEBUG: " + s)

def get_sound_file(instrument, note):
	return SOUNDS_DIR + '/' + instrument + '-' + note + '.wav'

def sound_play(note):
	global g_index_from_note
	fname = get_sound_file(g_instrument, note)
	channel = pygame.mixer.Channel(g_index_from_note[note])
	channel.play(pygame.mixer.Sound(fname))
	debug("start %s on channel %d\n" % (fname, g_index_from_note[note]))

def sound_stop(note):
	channel = pygame.mixer.Channel(g_index_from_note[note])
	channel.stop()
	debug("stop channel %d\n" % (g_index_from_note[note]))

def stair_down(stair_num):
	global g_power, g_note_from_stair
	if not g_power: return
	sound_play(g_note_from_stair[stair_num])

def stair_up(stair_num):
	global g_note_from_stair
	sound_play(g_note_from_stair[stair_num])

#key is the *major* key it's in.  It'll be centered on that note in octave 4
def set_key(key, include_accidentals):
	global g_note_from_stair, NSTAIRS

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
	min = center - NSTAIRS / 2

	# Reduce to NSTAIRS notes
	assert min >= 0 and len(notes) >= NSTAIRS
	g_note_from_stair = notes[min : NSTAIRS + min]
	assert len(g_note_from_stair) == NSTAIRS

def set_instrument(name):
	global g_instrument

	# We assume that the files were set up properly, so if C4 exists, the rest do as well
	fname = get_sound_file(name, 'C4')
	if not name in list_instruments():
		error("%s is not a valid instrument" % (name))
		return None

	g_instrument = name


# Should be possible to enable or disable the entire thing
def system_on():
	global g_power
	g_power = 1

def system_off():
	global power
	g_power = 0
	pygame.mixer.stop()

def play_song(fname):
	# easter egg: override the normal working and play a full song
	pass

def list_instruments():
	lst = list(set([ fname.split('-')[0] for fname in os.listdir(SOUNDS_DIR) ]))
	lst.sort()
	return lst

def init():
	global g_index_from_note

	pygame.mixer.pre_init(44100, -16, 2, 2048)
	pygame.mixer.init()
	pygame.mixer.set_num_channels(88)
	pygame.init()

	arr = [ 'C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab', 'A', 'Bb', 'B' ]
	allnotes = ["%s%d" % (note,octave) 
		for (i, (octave,note)) in enumerate(itertools.product(range(0, 9), arr)) 
	]
	allnotes = allnotes[allnotes.index('A0') : allnotes.index('C8') + 1]

	for i in range(0, len(allnotes)): g_index_from_note[allnotes[i]] = i

def cleanup():
	pygame.mixer.quit()

def test():
	init()

	for key in [ 'C', 'G', 'D', 'E', 'B', 'Gb', 'Db', 'Ab', 'Eb', 'Bb', 'F' ]:
		set_key(key, 0)
		sys.stdout.write("%2s: " % (key))
		print(set([ i[0:2] 
			for i in g_note_from_stair 
			if -1 != i.find('b') ]))

if '__main__' == __name__ :
	test()
