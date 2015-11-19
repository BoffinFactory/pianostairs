import pygame, itertools, collections

# Constants
NSTAIRS = 36

instrument='piano'
notes=[] # TODO: initialize to something
power=1 # if 0, nothing runs

# return a sound object based on the current instrument, as well as what note stair_num is connected to
def get_sound(stair_num):
	#TODO: notes needs to be a list containing things like 'C4', 'Bb2', etc
	#fname must exist.
	global instrument
	global notes
	fname=instrument + '-' + notes[stair_num] + '.wav'
	#TODO: verify that fname exists.  This should be a can't happen condition if the config functions check their args correctly.
	print("start %s" % (fname))
	return pygame.mixer.Sound(fname)
	pass

def stair_down(stair_num):
	global power
	if not power: return
	channel = pygame.mixer.Channel(stair_num)
	channel.play(get_sound(stair_num))
	print("on channel %d\n" % (stair_num))
	pass

def stair_up(stair_num):
	channel = pygame.mixer.Channel(stair_num)
	print("stop channel %d\n" % (stair_num))
	channel.stop()
	pass

#key is the *major* key it's in.  It'll be centered on that note in octave 4
def set_key(key, include_accidentals):
	global notes, NSTAIRS

	arr = [ "C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab", "A", "Bb", "B" ]
	basenotes = collections.deque(arr)
	basenotes.rotate(12 - arr.index(key))

	# 8 is just an upper bound. Beyond that, we can't center on C4 and the assertions will fail
	# But since outside that range is basically outside human hearing...
	arr = ["%s%d" % (note,octave) 
		for (i, (octave,note)) in enumerate(itertools.product(range(0, 8), basenotes)) 
		if include_accidentals or (i % 12 not in [ 1, 3, 6, 8, 10 ]) # filter accidentals
	]

	#Center on octave 4
	center = arr.index(key + "4")
	min = center - NSTAIRS / 2

	assert min >= 0 and len(arr) >= NSTAIRS
	notes = arr[min : NSTAIRS + min]
	assert len(notes) == NSTAIRS

	print key
	print set([ i[0:2] 
		for i in notes 
		if -1 != i.find("b") ])

# Should be possible to enable or disable the entire thing
def system_on():
	power=1

def system_off():
	power=0
	pygame.mixer.stop()

def play_song(fname):
	# easter egg: override the normal working and play a full song
	pass

def set_instrument(name):
	#TODO: verify that it's a valid instrument, and leave it unchanged otherwise
	instrument = name
	pass

def ui():
	#TODO: stick a keyboard on the wall to change settings.
	#And/or have it networked to boffin
	pass

def main():
	pygame.mixer.pre_init(44100, -16, 2, 2048)
	pygame.mixer.init()
	pygame.init()

	set_key("C", 0)
	set_key("G", 0)
	set_key("D", 0)
	set_key("A", 0)
	set_key("E", 0)
	set_key("B", 0)
	set_key("Gb", 0)
	set_key("Db", 0)
	set_key("Ab", 0)
	set_key("Eb", 0)
	set_key("Bb", 0)
	set_key("F", 0)

if "__main__" == __name__ :
	main()

