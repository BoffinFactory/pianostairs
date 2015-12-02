#!/usr/bin/python

import player, threading, collections, math
from ScrolledText import ScrolledText
from Tkinter import *
from  PIL import Image, ImageTk

def write(s):
	global ui
	ui.write(s)

class GUI:
	MAX_MESSAGES = 64
	PIANO_WIDTH = 1020
	PIANO_HEIGHT = PIANO_WIDTH / 10.625
	PIANO_BORDER = 10

	def __init__(self):
		self.messages = collections.deque(maxlen=self.MAX_MESSAGES)
		
	def noop():
		pass

	def write(self, s):
		self.messages.append(s)

		msg = ''
		for i in self.messages:
			msg = '%s\n%s' % (msg,i)

		#set text and scroll to end 
		self.output.delete(1.1, END)
		self.output.insert(END, msg)
		self.output.see(END)

	def draw_keyboard(self):
		""" draw standard 88 key piano, with each flight of stairs highlighted in a different color """
	
		def avg_color(color0, color1):
			""" takes colors in RGB hex form.  Average each component individually """
			def avg_byte(n):
				a = (color0 >> n) & 0xFF
				b = (color1 >> n) & 0xFF
				return ((a + b) / 2) << n
			
			return avg_byte(16) + avg_byte(8) + avg_byte(0)
		
		def draw_white_key(key):
			x0 = key * white_key_width + self.PIANO_BORDER
			x1 = x0 + white_key_width

			y0 = self.PIANO_BORDER
			y1 = y0 + white_key_height

			tone = chr(ord("A") + key % 7)
			octave = (key + 5) / 7
			note = tone + str(octave)

			color="white"
			outline="#888888"
			for i in range(0, len(flights)):
				if (note in flights[i]): 
					color = "#%06x" % avg_color(colors[i % len(colors)], 0xFFFFFF)
					outline = "#444444"

			self.canvas.create_rectangle(x0, y0, x1, y1, outline=outline, fill=color)
			#self.canvas.create_text(x0 + (x1-x0)/2, y0 + 0.8 * (y1-y0), text=note, fill="blue")

		def draw_black_key(key):
			""" key is the white key that this is the flat of """

			mod = key % 7
			if (2 == mod or 5 == mod): return

			x0 = key * white_key_width - black_key_width / 2 + self.PIANO_BORDER
			x1 = x0 + black_key_width

			y0 = self.PIANO_BORDER
			y1 = y0 + black_key_height
			
			tone = chr(ord("A") + key % 7)
			octave = (key + 5) / 7
			note = tone + "b" + str(octave)
		
			color="black"
			for i in range(0, len(flights)):
				if (note in flights[i]): 
					color = "#%06x" % avg_color(colors[i % len(colors)], 0x000000)

			self.canvas.create_rectangle(x0, y0, x1, y1, outline="grey", fill=color)
			#self.canvas.create_text(x0 + (x1-x0)/2, y0 + 5 + (y1-y0), text=note, fill="blue")

		max = int(math.ceil(len(player.g_notes) / player.STEPS_PER_FLIGHT))
		flights = [ player.g_notes[i * player.STEPS_PER_FLIGHT : (i + 1) * player.STEPS_PER_FLIGHT] for i in range(0, max) ]
		colors = ( 0x0000FF, 0x00FF00, 0xFF0000, 0x00FFFF, 0xFF00FF, 0xFFFF00 )

		white_key_width = self.PIANO_WIDTH / 52
		white_key_height = self.PIANO_HEIGHT

		black_key_width = white_key_width * 0.55
		black_key_height = self.PIANO_HEIGHT * 0.55

		self.canvas.delete("all")
		for key in range (0, 52): draw_white_key(key)
		for key in range (1, 52): draw_black_key(key)

	def run(self, f):
		global g_instrument

		def update_settings():
			player.set_instrument(selected_instrument.get())
			player.set_key(selected_key.get(), use_accidentals.get())
			self.draw_keyboard()

		#TODO: update status bar
		win = Tk()
		win.minsize(240, 320)
		frame = Frame(win)
		frame.pack(fill=BOTH, expand=1)
		#g.protocol('WM_DELETE_WINDOW', noop) # make window not closable
		win.title('pianostairs')

		# Menu
		menu = Menu(frame)
		menu_instrument = Menu(menu, tearoff=0)
		menu_key = Menu(menu, tearoff=0)
		
		selected_instrument = StringVar(menu_instrument)
		selected_instrument.set(player.g_instrument)
		selected_key = StringVar(menu_key)
		selected_key.set('C')
		use_accidentals = IntVar(menu)
		use_accidentals.set(0)

		for name in player.list_instruments():
			menu_instrument.add_radiobutton(label=name, command=update_settings, var=selected_instrument)
	
		menu_key.add_checkbutton(label='Include Accidentals', command=update_settings, var=use_accidentals)
		menu_key.add_separator()
		for key in [ 'C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab', 'A', 'Bb', 'B']:
			menu_key.add_radiobutton(label=key, command=update_settings, var=selected_key)
			
		menu.add_cascade(label='Instrument', menu=menu_instrument)
		menu.add_cascade(label='Key', menu=menu_key)
		
		self.output = ScrolledText(frame)
		self.output.pack(fill=BOTH)

		self.canvas = Canvas(height = self.PIANO_HEIGHT + 2 * self.PIANO_BORDER, 
			width=self.PIANO_WIDTH + 2 * self.PIANO_BORDER)
		self.canvas.pack(expand = YES, fill = BOTH)

		win.config(menu=menu)
		update_settings()

		win.after(0, f)
		win.mainloop()

ui = GUI()

def f():
	print "I'm going to be replaced by the code that decodes the pin input and calls the stuff in player.py!"

if '__main__' == __name__ :
	ui.run(f)

