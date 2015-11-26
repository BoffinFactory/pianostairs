import pygame, itertools, collections, sys, os, gui

# Constants
NSTAIRS = 32
STEPS_PER_FLIGHT = 16
SOUNDS_DIR = 'sounds'
DEBUG = 1

# Globals. Don't modify these directly.  set_(key|instrument) and power_(on|off) run additional checks and/or do stuff.
g_instrument = 'piano'
g_notes = []
g_power = 1 # if 0, nothing runs


# Output functions.  Depending on the physical interface, I might want these doing different things
def output(s):
	global gui
	gui.write(s)

def error(s):
	output("ERROR: " + s)

def debug(s):
	global DEBUG
	if DEBUG: output("DEBUG: " + s)


def get_sound_file(instrument, note):
	return SOUNDS_DIR + '/' + instrument + '-' + note + '.wav'

def stair_down(stair_num):
	global g_power, g_notes
	
	if not g_power: return

	channel = pygame.mixer.Channel(stair_num)
	fname = get_sound_file(g_instrument, g_notes[stair_num])

	channel.play(pygame.mixer.Sound(fname))
	debug("start %s on channel %d\n" % (fname, stair_num))

def stair_up(stair_num):
	channel = pygame.mixer.Channel(stair_num)
	channel.stop()
	debug("stop channel %d\n" % (stair_num))


#key is the *major* key it's in.  It'll be centered on that note in octave 4
def set_key(key, include_accidentals):
	global g_notes, NSTAIRS

	arr = [ 'C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab', 'A', 'Bb', 'B' ]

	if key not in arr:
		error("key %s is invalid.  Select one of %s" % (key, arr))
		return -1

	basenotes = collections.deque(arr)
	basenotes.rotate(12 - arr.index(key))

	# 8 is just an upper bound. Beyond that, we can't center on C4 and the assertions will fail
	# But since outside that range is basically outside human hearing...
	notes = ["%s%d" % (note,octave) 
		for (i, (octave,note)) in enumerate(itertools.product(range(0, 8), basenotes)) 
		if include_accidentals or (i % 12 not in [ 1, 3, 6, 8, 10 ]) # filter accidentals
	]

	# Center on octave 4
	center = notes.index(key + '4')
	min = center - NSTAIRS / 2

	# Reduce to NSTAIRS notes
	assert min >= 0 and len(notes) >= NSTAIRS
	g_notes = notes[min : NSTAIRS + min]
	assert len(g_notes) == NSTAIRS

	return 0

def set_instrument(name):
	global g_instrument

	# We assume that the files were set up properly, so if C4 exists, the rest do as well
	fname = get_sound_file(name, 'C4')
	if not name in list_instruments():
	#if not os.path.isfile(fname):
		error("%s is not a valid instrument" % (name))
		return -1

	g_instrument = name
	return 0


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

def ui():
	#TODO: stick a keyboard and small lcd display or something on the wall to change settings
	#And/or have it networked to boffin
	pass

def init():
	pygame.mixer.pre_init(44100, -16, 2, 2048)
	pygame.mixer.init()
	pygame.init()
	set_key('C', 0)

def cleanup():
	pygame.mixer.quit()

def main():
	init()

	while (1):
		try:
			ui()
		except:
			# Should never happen, so if it does, just do a soft reset
			cleanup()
			init()

	#for key in [ 'C', 'G', 'D', 'E', 'B', 'Gb', 'Db', 'Ab', 'Db', 'Ab', 'Eb', 'Bb', 'F' ]:
	#	set_key(key, 0)
	#	sys.stdout.write("%2s: " % (key))
	#	debug(set([ i[0:2] 
	#		for i in notes 
	#		if -1 != i.find('b') ]))

#if '__main__' == __name__ :
#	main()

