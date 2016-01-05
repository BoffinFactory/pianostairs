import config as G, pygame, itertools, collections, sys, os, gui

def get_sound_file(instrument, note):
	return G.SOUNDS_DIR + '/' + instrument + '-' + note + '.wav'

def sound_play(note):
	if G.mute: return

	fname = get_sound_file(G.instrument, note)
	if not os.path.isfile(fname):
		G.error('File not found: ' + fname)
		return
	channel = pygame.mixer.Channel(G.index_from_note[note])
	sound = pygame.mixer.Sound(fname)
	sound.set_volume(G.volume)
	channel.play(sound)
	G.output('Play %s' % (note))
	G.debug("start %s on channel %d at volume %.1f" % (fname, G.index_from_note[note], 11.0 * G.volume))

def sound_stop(note):
	channel = pygame.mixer.Channel(G.index_from_note[note])
	channel.stop()
	G.debug("stop channel %d" % (G.index_from_note[note]))

def stair_down(stair_num):
	if G.mute: return
	note = G.note_from_stair[stair_num]
	G.gui.key_down(note)
	sound_play(note)

def stair_up(stair_num):
	note = G.note_from_stair[stair_num]
	G.gui.key_up(note)
	sound_stop(note)

#key is the *major* key it's in.  It'll be centered on that note in octave 4
def set_key(key, include_accidentals):
	arr = [ 'C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab', 'A', 'Bb', 'B' ]

	if key not in arr:
		G.error("key %s is invalid.  Select one of %s" % (key, arr))
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

	if G.gui:
		G.gui.selected_key.set(key)
		G.gui.use_accidentals.set(include_accidentals)
		G.gui.draw_keyboard()

	if include_accidentals:
		G.output('Include all notes (centered on %s)' % (key))
	else:
		G.output('Key = %s' % (key))

def set_instrument(name):
	# We assume that the files were set up properly, so if C4 exists, the rest do as well
	name = name.replace(' ', '_')
	fname = get_sound_file(name, 'C4')
	if not name in list_instruments():
		G.error("%s is not a valid instrument" % (name))
		return None

	G.instrument = name
	if G.gui: G.gui.selected_instrument.set(G.instrument)
	G.output('Instrument = ' + G.instrument.replace('_', ' '))


# Should be possible to enable or disable the entire thing
def sound_on():
	G.mute = 0

def sound_off():
	G.mute = 1
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
