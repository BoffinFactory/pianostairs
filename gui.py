import config as G, player, threading, collections, math, sys, parser
from ScrolledText import ScrolledText
from Tkinter import *
from  PIL import Image, ImageTk
	
#def close_window():
#	sys.exit()

class GUI:
	MAX_MESSAGES = 64
	PIANO_WIDTH = 1020
	PIANO_HEIGHT = PIANO_WIDTH / 10.625
	PIANO_BORDER = 10

	def write(self, s):
		self.messages.append(s)

		msg = ''
		for i in self.messages:
			msg = '%s\n%s' % (msg,i)

		#set text and scroll to end 
		self.output.delete(1.1, END)
		self.output.insert(END, msg)
		self.output.see(END)

	def press_key(self, note):
		self.write(note)
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
			button = Button(self.canvas, 
				highlightbackground=outline, bg="#%06x" % (color),
				highlightcolor=outline, activebackground="#%06x" % (active_color),
				borderwidth=1, highlightthickness=0,
				command=lambda : self.press_key(note))
			button.place(x=x0, y=y0, width=x1-x0, height=y1-y0)

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
			active_color = avg_color(avg_color(color, 0xFFFFFF), 0xFFFFFF)
			button = Button(self.canvas, 
				highlightbackground="grey", bg="#%06x" % (color),
				highlightcolor="grey", activebackground="#%06x" % (active_color),
				borderwidth=1, highlightthickness=0,
				command=lambda : self.press_key(note))
			button.place(x=x0, y=y0, width=x1-x0, height=y1-y0)

		max = int(math.ceil(len(G.note_from_stair) / G.STEPS_PER_FLIGHT))
		flights = [ G.note_from_stair[i * G.STEPS_PER_FLIGHT : (i + 1) * G.STEPS_PER_FLIGHT] for i in range(0, max) ]
		colors = ( 0x0000FF, 0x00FF00, 0xFF0000, 0x00FFFF, 0xFF00FF, 0xFFFF00 )

		white_key_width = self.PIANO_WIDTH / 52
		white_key_height = self.PIANO_HEIGHT

		black_key_width = white_key_width * 0.55
		black_key_height = self.PIANO_HEIGHT * 0.55

		self.canvas.delete("all")
		for key in range (0, 52): draw_white_key(key)
		for key in range (1, 52): draw_black_key(key)
	
	def __init__(self):
		def update_settings():
			player.set_instrument(self.selected_instrument.get())
			player.set_key(selected_key.get(), use_accidentals.get())
			self.draw_keyboard()

		def toggle_power():
			if (mute_button.get()):
				player.system_on()
			else:
				player.system_off()

		self.messages = collections.deque(maxlen=self.MAX_MESSAGES)
		self.win = Tk()
		self.win.minsize(240, 320)
		self.frame = Frame(self.win)
		self.frame.pack(fill=BOTH, expand=1)
		#self.win.protocol('WM_DELETE_WINDOW', close_window)
		self.win.title('pianostairs')

	
		buttons = Frame(self.frame)
		buttons.pack(fill=BOTH)

		mute_button = IntVar(buttons)
		mute_button.set(0)

		mute = Checkbutton(master=buttons, text=' Mute ', indicatoron=0, var=mute_button,
			command=lambda: player.system_off() if mute_button.get() else player.system_on())
		mute.pack(side=LEFT)
	
		self.demo_button = IntVar(buttons)
		self.demo_button.set(0)
		demo = Checkbutton(master=buttons, text=' Demo ', indicatoron=0, var=self.demo_button,
			command=lambda: parser.playsong('copeland.score'))
		demo.pack(side=LEFT)

		self.output = ScrolledText(self.frame)
		self.output.pack(fill=BOTH)

		# Menu
		menu = Menu(self.frame)
		menu_instrument = Menu(menu, tearoff=0)
		menu_key = Menu(menu, tearoff=0)
		
		self.selected_instrument = StringVar(menu_instrument)
		self.selected_instrument.set(G.instrument)
		selected_key = StringVar(menu_key)
		selected_key.set('C')
		use_accidentals = IntVar(menu)
		use_accidentals.set(0)

		for name in player.list_instruments():
			menu_instrument.add_radiobutton(label=name, command=update_settings, var=self.selected_instrument)
	
		menu_key.add_checkbutton(label='Include Accidentals', command=update_settings, var=use_accidentals)
		menu_key.add_separator()
		for key in [ 'C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab', 'A', 'Bb', 'B']:
			menu_key.add_radiobutton(label=key, command=update_settings, var=selected_key)
			
		menu.add_cascade(label='Instrument', menu=menu_instrument)
		menu.add_cascade(label='Key', menu=menu_key)
		

		self.canvas = Canvas(height = self.PIANO_HEIGHT + 2 * self.PIANO_BORDER, 
			width=self.PIANO_WIDTH + 2 * self.PIANO_BORDER)
		self.canvas.pack(expand = YES, fill = BOTH)

		self.win.config(menu=menu)
		update_settings()

def run(f):
	G.gui = GUI()
	G.gui.win.after(0, f)
	G.gui.win.mainloop()


