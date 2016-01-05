import config as G, player, threading, collections, math, sys, parser, pygame
from ScrolledText import ScrolledText
from Tkinter import *
from  PIL import Image, ImageTk

class GUI:
	MAX_MESSAGES = 1024 # Fine if it's large, but it should be finite to avoid running out of memory
	PIANO_WIDTH = 0
	PIANO_HEIGHT = 0
	PIANO_BORDER = 10
	keys = {}

	def write(self, s):
		self.messages.append(s)

		msg = ''
		for i in self.messages:
			msg = '%s\n%s' % (msg,i)

		#set text and scroll to end 
		self.output.delete(1.1, END)
		self.output.insert(END, msg)
		self.output.see(END)

	def key_up(self, note):
		color = self.keys[note].config('disabledforeground')[4]
		self.keys[note].config(relief=RAISED)
		self.keys[note].config(background=color)

	def key_down(self, note):
		color = self.keys[note].config('activebackground')[4]
		self.keys[note].config(relief=SUNKEN)
		self.keys[note].config(background=color)

	def press_key(self, note):
		player.sound_play(note)

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

			color = 0xFFFFFF
			outline = "#888888"
			for i in range(0, len(flights)):
				if (note in flights[i]): 
					color = avg_color(colors[i % len(colors)], 0xFFFFFF)
					outline = "#444444"

			#self.canvas.create_rectangle(x0, y0, x1, y1, outline=outline, fill="#%06x" % (color))
			#self.canvas.create_text(x0 + (x1-x0)/2, y0 + 0.8 * (y1-y0), text=note, fill="blue")
			
			active_color = avg_color(color, 0xCCCCCC)
			self.keys[note] = Button(self.canvas, 
				highlightbackground=outline, bg="#%06x" % (color),
				highlightcolor=outline, activebackground="#%06x" % (active_color),
				disabledforeground="#%06x" % (color), # kludge to store it
				borderwidth=1, highlightthickness=0,
				command=lambda : self.press_key(note))
			self.keys[note].place(x=x0, y=y0, width=x1-x0, height=y1-y0)

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
		
			color=0x000000
			for i in range(0, len(flights)):
				if (note in flights[i]): 
					color = avg_color(colors[i % len(colors)], 0x000000)

			#self.canvas.create_rectangle(x0, y0, x1, y1, outline="grey", fill="#%06x" % (color))
			#self.canvas.create_text(x0 + (x1-x0)/2, y0 + 5 + (y1-y0), text=note, fill="blue")

			active_color = avg_color(color, 0xFFFFFF)
			self.keys[note] = Button(self.canvas, 
				highlightbackground="grey", bg="#%06x" % (color),
				highlightcolor="grey", activebackground="#%06x" % (active_color),
				disabledforeground="#%06x" % (color), # kludge to store it
				borderwidth=1, highlightthickness=0,
				command=lambda : self.press_key(note))
			self.keys[note].place(x=x0, y=y0, width=x1-x0, height=y1-y0)

		max = int(math.ceil(len(G.note_from_stair) / G.STEPS_PER_FLIGHT))
		flights = [ G.note_from_stair[i * G.STEPS_PER_FLIGHT : (i + 1) * G.STEPS_PER_FLIGHT] for i in range(0, max) ]
		colors = ( 0x0000FF, 0x00FF00, 0xFF0000, 0x00FFFF, 0xFF00FF, 0xFFFF00 )

		white_key_width = self.PIANO_WIDTH / 52
		white_key_height = self.PIANO_HEIGHT

		black_key_width = white_key_width * 0.55
		black_key_height = self.PIANO_HEIGHT * 0.55

		# The actual border size will vary a bit, since white_key_width is restricted to integers.
		# This is preferable to what it looks like otherwise
		self.canvas.destroy()
		self.canvas = Canvas(self.frame, 
			height = self.PIANO_HEIGHT + 2 * self.PIANO_BORDER,
			width = self.PIANO_WIDTH)
		self.canvas.pack(side=BOTTOM)
		for key in range (0, 52): draw_white_key(key)
		for key in range (1, 52): draw_black_key(key)
	
	def resize(self, event):
		self.PIANO_WIDTH = self.win.winfo_width() - 2 * self.PIANO_BORDER
		self.PIANO_HEIGHT = self.PIANO_WIDTH / 10.625
		self.draw_keyboard()

	def __init__(self):
		def update_settings():
			player.set_instrument(self.selected_instrument.get())
			player.set_key(self.selected_key.get(), self.use_accidentals.get())
			self.resize(None)

		def toggle_power():
			if (mute_button.get()):
				player.sound_on()
			else:
				player.sound_off()

		self.messages = collections.deque(maxlen=self.MAX_MESSAGES)
		self.win = Tk()
		if G.DISABLE_CLOSE_BUTTON: self.win.overrideredirect(1)
		self.win.attributes('-fullscreen', 1)
		self.win.minsize(640, 540)
		self.frame = Frame(self.win)
		self.frame.pack(fill=BOTH, expand=1)
		self.win.title('pianostairs')
	
		buttons = Frame(self.frame)
		buttons.pack(side=TOP, fill=X)

		mute_button = IntVar()
		mute_button.set(0)

		mute = Checkbutton(master=buttons, text=' Mute ', indicatoron=0, var=mute_button,
			command=lambda: player.sound_off() if mute_button.get() else player.sound_on())
		mute.pack(side=LEFT)
	
		self.demo_button = IntVar()
		self.demo_button.set(0)
		def toggle_demo():
			if self.demo_button.get():
				parser.playsong('copeland.score')
			else:
				self.draw_keyboard() # reset any active buttons

		demo = Checkbutton(master=buttons, text=' Demo ', indicatoron=0, var=self.demo_button,
			command=toggle_demo)
		demo.pack(side=LEFT)
		
		#Volume control	
		vol_frame = Frame(buttons)
		volume = DoubleVar()
		def set_volume(*args):
			G.volume = volume.get() / 11.0
		volume.trace("w", set_volume)
		volume.set(10.0)
		Label(vol_frame, text='  Volume: ').pack(side=LEFT)
		Scale(vol_frame, showvalue=0, from_=0, to=11, resolution=.1, 
			length=220, orient=HORIZONTAL, variable=volume).pack(side=LEFT)
		Label(vol_frame, textvariable=volume, width=4).pack(side=LEFT)
		vol_frame.pack(side=RIGHT)

		self.output = ScrolledText(self.frame)
		self.output.pack(fill=BOTH, expand = 1)

		# Menu
		menu = Menu(self.frame)
		menu_instrument = Menu(menu, tearoff=0)
		menu_key = Menu(menu, tearoff=0)
		
		self.selected_instrument = StringVar()
		self.selected_instrument.set(G.instrument)
		self.selected_key = StringVar()
		self.selected_key.set('C')
		self.use_accidentals = IntVar()
		self.use_accidentals.set(0)

		for name in player.list_instruments():
			menu_instrument.add_radiobutton(label=name.replace('_',' '), command=update_settings, var=self.selected_instrument)
	
		menu_key.add_checkbutton(label='Include Accidentals', command=update_settings, var=self.use_accidentals)
		menu_key.add_separator()
		for key in [ 'C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab', 'A', 'Bb', 'B']:
			menu_key.add_radiobutton(label=key, command=update_settings, var=self.selected_key)
			
		menu.add_cascade(label='Instrument', menu=menu_instrument)
		menu.add_cascade(label='Key', menu=menu_key)
		
		self.frame.bind('<Configure>', self.resize)
		self.canvas = Canvas(self.frame)

		self.win.config(menu=menu)
		update_settings()

def run(f):
	G.gui = GUI()
	G.gui.win.after(0, f)
	G.gui.win.mainloop()


