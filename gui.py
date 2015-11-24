import player, threading, collections
from ScrolledText import ScrolledText
from Tkinter import *

MAX_MESSAGES = 64

def write(s):
	global ui
	ui.write(s)

class GUI(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
		self.messages = collections.deque(maxlen=MAX_MESSAGES)
		
	def noop():
		pass

	def write(self, s):
		#TODO: keep N lines of output, and just delete them after they scroll off the top
		global MAX_MESSAGES
		self.messages.append(s)

		msg = ''
		for i in self.messages:
			print i
			msg = '%s\n%s' % (msg,i)

		#set text and scroll to end 
		self.output.delete(1.1, END)
		self.output.insert(END, msg)
		self.output.see(END)

	def run(self):
		def update_settings():
			player.set_instrument(selected_instrument.get())
			player.set_key(selected_key.get(), use_accidentals.get())

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
		selected_instrument.set('piano')
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

		win.config(menu=menu)
		update_settings()

		win.geometry('{}x{}'.format(320, 200))
		win.mainloop()

ui = GUI()

if '__main__' == __name__ :
	ui.start()
	ui.join()
	
