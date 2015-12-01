#!/usr/bin/python

import player, threading, collections
from ScrolledText import ScrolledText
from Tkinter import *
from  PIL import Image, ImageTk

MAX_MESSAGES = 64

def write(s):
	global ui
	ui.write(s)

class GUI:
	def __init__(self):
		self.messages = collections.deque(maxlen=MAX_MESSAGES)
		
	def noop():
		pass

	def write(self, s):
		#TODO: keep N lines of output, and just delete them after they scroll off the top
		global MAX_MESSAGES
		self.messages.append(s)

		msg = ''
		for i in self.messages:
			#print i
			msg = '%s\n%s' % (msg,i)

		#set text and scroll to end 
		self.output.delete(1.1, END)
		self.output.insert(END, msg)
		self.output.see(END)

	def find_key(self, note):
		#TODO: rather than trying to match this up perfectly to an existing image,
		#just draw the image directly.  Then the keys will have uniform width
		#In fact, I might even be able to replace the rectangles with Buttons
		KEY_ORIGIN = (23, 69)#, 12, 20)
		KEY_WIDTH = 9.8
		KEY_HEIGHT = 49
		KEY_BLACK_OFFSET = (3, 24) # e.g. Ab's lower left corner is A's lower left corner minus this
		KEY_BLACK_WIDTH = 5

		tone = (ord(note[0]) - ord('C')) % 8
		flat = len(note) == 3
		octave = ord(note[len(note) - 1]) - ord('0')

		(x0, y0) = KEY_ORIGIN
		#x0 += (tone) * KEY_WIDTH
		x0 += (7 * (octave - 1)  +  tone) * KEY_WIDTH
		y1 = y0 - KEY_HEIGHT
		if (flat): 
			(x0, y0) = (x0 - KEY_BLACK_OFFSET[0], y0 - KEY_BLACK_OFFSET[1])
			x1 = x0 + KEY_BLACK_WIDTH
		else:
			x1 = x0 + KEY_WIDTH

		#return (3, 69, 12, 20)
		return (x0, y0, x1, y1)

	def run(self, f):
		global g_instrument

		def update_settings():
			player.set_instrument(selected_instrument.get())
			player.set_key(selected_key.get(), use_accidentals.get())
		
			(x0, y0, x1, y1) = ui.find_key(selected_key.get() + "4")

			canvas.delete("all")
			self.image = ImageTk.PhotoImage(file = "keyboard.png")
			canvas.create_image(0, 0, image = self.image, anchor = NW)
			canvas.create_rectangle(x0, y0, x1, y1, outline="blue")

			write(player.g_notes)

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
	
		menu_key.add_checkbutton(label='Use Accidentals', command=update_settings, var=use_accidentals)
		menu_key.add_separator()
		for key in [ 'C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab', 'A', 'Bb', 'B']:
			menu_key.add_radiobutton(label=key, command=update_settings, var=selected_key)
			
		menu.add_cascade(label='Instrument', menu=menu_instrument)
		menu.add_cascade(label='Key', menu=menu_key)
		
		self.output = ScrolledText(frame)
		self.output.pack(fill=BOTH)

		self.image = ImageTk.PhotoImage(file = "keyboard.png")
		canvas = Canvas(height = self.image.height(), width=self.image.width())
		canvas.create_image(0, 0, image = self.image, anchor = NW)
		canvas.pack(expand = YES, fill = BOTH)

		win.config(menu=menu)
		update_settings()

		#win.geometry('{}x{}'.format(320, 200))
		win.after(0, f)
		win.mainloop()

ui = GUI()

def f():
	print "I'm going to be replaced by the code that decodes the pin input and calls the stuff in player.py!"

if '__main__' == __name__ :
	ui.run(f)

