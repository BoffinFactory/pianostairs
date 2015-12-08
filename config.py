# Constants
NSTAIRS = 32
STEPS_PER_FLIGHT = 16
SOUNDS_DIR = 'sounds'
DEBUG = 0

# Globals. Don't modify these directly.  set_(key|instrument) and power_(on|off) run additional checks and/or do stuff.
instrument = 'piano'
note_from_stair = []
index_from_note = {}
power = 1 # if 0, nothing runs

gui = None

