import re, threading, config as G, player, pygame
import sys, traceback

# Note syntax: (C4 C5)2. means a dotted 1/2 note chord of C4 and C5.
# If a note is prefixed with ~, it means it's tied from the previous
# one and isn't restarted

def playsong_aux(fname):
	infile = open(fname, 'r')
	tempo = 120 # andante
	prev_tones = []
	line = ''

	while G.gui and G.gui.demo_button.get():
		line = line.strip()
		#G.output('parse line: "%s"' % (line))

		if (not len(line)):
			line = infile.readline()
			if ('' == line):
				pygame.mixer.stop()
				return None
		elif re.match(r'#', line):
			G.debug(line)
			line = ''
		elif re.match(r'\\tempo ([1-9][0-9]*)\s*$', line):
			# Yay! I get to pointlessly repeat myself because python doesn't trust the programmer with assignments that evaluate to a value!
			matches = re.match(r'\\tempo ([1-9][0-9]*)\s*$', line)
			try:
				tempo = int(matches.group(1))
				G.output('Tempo = %s' % (tempo))
			except:
				G.error("Can't happen. Invalid tempo: \"" + line + '"')
			line = ''
		elif re.match(r'\\instrument (.*)', line):
			matches = re.match(r'\\instrument (.*)', line)
			player.set_instrument(matches.group(1))
			line = '' # instruments can have spaces, so this command always uses the entire line
		elif re.match(r'\(([~A-G0-8b ]*)\)([1-9][0-9]*\.?)(.*)', line): 
			matches = re.match(r'\(([~A-G0-8b ]*)\)([1-9][0-9]*\.?)(.*)', line)
			# Does admit a few notes that aren't on the keyboard, like G8, but those will get caught by sound_play()
			# Also admits things like (C4~3 A)3. If I can nest groups, I *could* catch those, but again, sound_play will handle it.
			# The checks here just need to make sure it doesn't do anything that could escape the SOUNDS_DIR
			tones = matches.group(1).split()
			try:
				s = matches.group(2)
				duration = 4.0 / float(s) # now equals number of quarter notes
				if '.' == s[len(s) - 1]: # dotted note
					duration = duration * 1.5;
				
				# Stop the previous set of notes
				for tone in prev_tones:
					if ('~' + tone) not in tones:
						player.sound_stop(tone)

				# Play this set
				for (i, tone) in enumerate(tones):
					if ('~' != tone[0]):
						# If it's a tie, we don't start it over
						player.sound_play(tone)
					else:
						tones[i] = tone[1:len(tone)] # prev_tones won't care if it was already a tie

				prev_tones = tones
				
				# (duration beats) / (tempo beats/minute) * 60 s/min* 1000 ms/s = x ms
				ms = int(1000 * 60 * duration / tempo)
				pygame.time.delay(ms)
				line = matches.group(3)
			except:
				G.error('Invalid note: "' + line + '"')
				print sys.exc_info()
				traceback.print_tb(sys.exc_info()[2])
				print ''

				line = ''
		else:
			G.error('Syntax error: "' + line + '"')
			line = ''

	pygame.mixer.stop()

def playsong(fname):
	t = threading.Thread(target=playsong_aux, args=(fname,))
	t.start()

