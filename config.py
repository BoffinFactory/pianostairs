# Constants
NSTAIRS = 32
STEPS_PER_FLIGHT = 16
SOUNDS_DIR = 'sounds'
DEBUG = 0
DISABLE_CLOSE_BUTTON = 0
ACTIVE_LOW = 1

# Globals. Don't modify these directly.  set_(key|instrument) and sound_(on|off) run additional checks and/or do stuff.
instrument = 'piano'
note_from_stair = []
index_from_note = {}
mute = 0 # if 0, nothing runs

gui = None #GUI
volume = 0.0

# Output functions.  Depending on the physical interface, I might want these doing different things
def output(s):
	if gui:
		gui.write(s)
	else:
		print(s)

def error(s):
	output("ERROR: " + s)

def debug(s):
	if DEBUG: output("DEBUG: " + s)
	
