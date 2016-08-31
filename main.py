#!/usr/bin/python
import config as G, gui, player
import parser, serial, thread

# TODO: Find docs on ser.readline and find out why it didn't work this way
def readline(ser):
	line = ""
	while 1:
		c = ser.read()
		if not len(c) or '\r' == c: continue
		if '\n' == c: return line
		line = line + c

def interface():
	ser = serial.Serial(
		port='/dev/ttyACM0',
		baudrate = 9600,
		parity = serial.PARITY_NONE,
		stopbits = serial.STOPBITS_ONE,
		bytesize = serial.EIGHTBITS,
		timeout = 0)

	G.output("connected to: " + ser.portstr)

	prev = (G.ACTIVE_LOW << G.NSTAIRS) - 1  # assume all stairs are up to begin with

	while 1:
		line = readline(ser)
		G.debug("read " + line)
		n = int(line, 16)

		# pitch increases with stair number
		for bit in range(0, G.NSTAIRS):
			if ((n ^ prev) >> bit) & 1: # only call player if the stair has changed state
				if G.ACTIVE_LOW != ((n >> bit) & 1):
					player.stair_down(bit)
				else:
					player.stair_up(bit)

		prev = n

def start_interface():
	thread.start_new_thread(interface, ());

player.init()
gui.run(start_interface)

