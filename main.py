#!/usr/bin/python
import config as G, gui, player
import parser

def interface():
	ser = serial.Serial(
		port='/dev/ttyACM0',
		baudrate = 9600,
		parity = serial.PARITY_NONE,
		stopbits = serial.STOPBITS_ONE,
		bytesize = serial.EIGHTBITS,
		timeout = 0)

	G.gui.write("connected to: " + ser.portstr)

	prev = (G.ACTIVE_LOW << G.NSTAIRS) - 1  # assume all stairs are up to begin with
	for line in ser.readline():
		n = int(line.strip(), 16)

		# pitch increases with stair number
		for bit in range(0, G.NSTAIRS):
			if ((n ^ prev) >> bit) & 1: # only call player if the stair has changed state
				if G.ACTIVE_LOW != ((n >> bit) & 1):
					player.stair_down(bit)
				else:
					player.stair_up(bit)

		prev = n

player.init()
gui.run(interface)

