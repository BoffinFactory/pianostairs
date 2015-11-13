import serial
import pygame
def setup(ser):
	ser = serial.Serial(
		port='/dev/ttyACM0',\
		baudrate=9600,\
		parity=serial.PARITY_NONE,\
		stopbits=serial.STOPBITS_ONE,\
		bytesize=serial.EIGHTBITS,\
		timeout=0)
	print("connected to: " + ser.portstr)
	return ser
def readSerial(ser,line,sounds):

	for c in ser.read():
		if (c != '\r' and c != '\n'):
			line.append(c)
		if c == '\n':
			#print line
			decodeHex(line,sounds)
			del line[:]
			break
def play():
	
	pygame.mixer.pre_init(44100, -16, 2, 2048)
	pygame.mixer.init()
	pygame.init()
	#print "hey I finaly got this working!"
	allsounds = []
	sounds = []
	sounds.append([False,pygame.mixer.Sound('39179__jobro__piano-ff-032.wav')])
	sounds.append([False,pygame.mixer.Sound('39178__jobro__piano-ff-031.wav')])
	sounds.append([False,pygame.mixer.Sound('39177__jobro__piano-ff-030.wav')])
	sounds.append([False,pygame.mixer.Sound('39176__jobro__piano-ff-029.wav')])
	allsounds.append(sounds)
	sounds2 = []
	sounds2.append([False,pygame.mixer.Sound('39175__jobro__piano-ff-028.wav')])
	sounds2.append([False,pygame.mixer.Sound('39174__jobro__piano-ff-027.wav')])
	sounds2.append([False,pygame.mixer.Sound('39173__jobro__piano-ff-026.wav')])
	sounds2.append([False,pygame.mixer.Sound('39172__jobro__piano-ff-025.wav')])
	allsounds.append(sounds2)
	sounds3 = []
	sounds3.append([False,pygame.mixer.Sound('39171__jobro__piano-ff-024.wav')])
	sounds3.append([False,pygame.mixer.Sound('39170__jobro__piano-ff-023.wav')])
	sounds3.append([False,pygame.mixer.Sound('39169__jobro__piano-ff-022.wav')])
	sounds3.append([False,pygame.mixer.Sound('39168__jobro__piano-ff-021.wav')])
	allsounds.append(sounds3)
	sounds4 = []
	sounds4.append([False,pygame.mixer.Sound('39167__jobro__piano-ff-020.wav')])
	sounds4.append([False,pygame.mixer.Sound('39166__jobro__piano-ff-019.wav')])
	sounds4.append([False,pygame.mixer.Sound('39165__jobro__piano-ff-018.wav')])
	sounds4.append([False,pygame.mixer.Sound('39164__jobro__piano-ff-017.wav')])
	allsounds.append(sounds4)
	sounds5 = []
	sounds5.append([False,pygame.mixer.Sound('39163__jobro__piano-ff-016.wav')])
	sounds5.append([False,pygame.mixer.Sound('39162__jobro__piano-ff-015.wav')])
	sounds5.append([False,pygame.mixer.Sound('39161__jobro__piano-ff-014.wav')])
	sounds5.append([False,pygame.mixer.Sound('39160__jobro__piano-ff-013.wav')])
	allsounds.append(sounds5)
	sounds6 = []
	sounds6.append([False,pygame.mixer.Sound('39159__jobro__piano-ff-012.wav')])
	sounds6.append([False,pygame.mixer.Sound('39158__jobro__piano-ff-011.wav')])
	sounds6.append([False,pygame.mixer.Sound('39157__jobro__piano-ff-010.wav')])
	sounds6.append([False,pygame.mixer.Sound('39156__jobro__piano-ff-009.wav')])
	allsounds.append(sounds6)
	sounds7 = []
	sounds7.append([False,pygame.mixer.Sound('39155__jobro__piano-ff-008.wav')])
	sounds7.append([False,pygame.mixer.Sound('39154__jobro__piano-ff-007.wav')])
	sounds7.append([False,pygame.mixer.Sound('39153__jobro__piano-ff-006.wav')])
	sounds7.append([False,pygame.mixer.Sound('39152__jobro__piano-ff-005.wav')])
	allsounds.append(sounds7)
	sounds8 = []
	sounds8.append([False,pygame.mixer.Sound('39151__jobro__piano-ff-004.wav')])
	sounds8.append([False,pygame.mixer.Sound('39150__jobro__piano-ff-003.wav')])
	sounds8.append([False,pygame.mixer.Sound('39149__jobro__piano-ff-002.wav')])
	sounds8.append([False,pygame.mixer.Sound('39148__jobro__piano-ff-001.wav')])
	allsounds.append(sounds8)
	return allsounds

def decodeHex(line,sounds):
	u = 0
	for index,word in enumerate(reversed(line)):
		

		scale = 16 ## equals to hexadecimal

		num_of_bits = 4
		for idx, bit in enumerate(reversed(bin(int(word, scale))[2:].zfill(num_of_bits))):
			if bit == '1' and not sounds[index][idx][0]:
				sounds[index][idx][1].play()
				sounds[index][idx][0] = True

			elif bit == '0' and sounds[index][idx][0]:
				sounds[index][idx][1].stop()
				sounds[index][idx][0] = False
				


if __name__ == "__main__":
	ser = None
	ser = setup(ser)
	line = []
	sounds = play()
	while True:
		readSerial(ser,line,sounds)
	ser.close()