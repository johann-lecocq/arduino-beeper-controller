#!/bin/python2

__author__ = "Johann Lecocq(johann-lecocq.fr)"
__license__ = "GNU GENERAL PUBLIC LICENSE version 2"
__version__ = "1.0"

import serial
import threading
from time import sleep
from sys import argv,exit

FREQUENCES=[[16, 33, 65, 131, 262, 523, 1046, 2093, 4186],
    [17, 35, 69, 139, 277, 554, 1109, 2217, 4435],
    [18, 37, 73, 147, 294, 587, 1175, 2349, 4699],
    [19, 39, 78, 155, 311, 622, 1244, 2489, 4978],
    [21, 41, 82, 165, 330, 659, 1328, 2637, 5274],
    [22, 44, 87, 175, 349, 698, 1397, 2794, 5588],
    [23, 46, 92, 185, 370, 740, 1480, 2960, 5920],
    [24, 49, 98, 196, 392, 784, 1568, 3136, 6271],
    [26, 52, 104, 208, 415, 831, 1661, 3322, 6645],
    [27, 55, 110, 220, 440, 880, 1760, 3520, 7040],
    [29, 58, 116, 233, 466, 932, 1865, 3729, 7459],
    [31, 62, 123, 245, 494, 988, 1975, 3951, 7902]]

NOTES=["DO","DO_","RE","RE_","MI","FA","FA_","SOL","SOL_","LA","LA_","SI","_"]

def joue(octave,note,longueur):
	global tempo,ser
	d=((octave) &0x0F)<<4 | (note &0x0F)
	ser.write(chr(d))
	ser.write(chr(longueur>>8))
	ser.write(chr(longueur & 0xFF))
	print d,longueur>>8,longueur & 0xFF
	sleep(longueur/1000.0)

tempo=1000
note=0
octave=4
longueur=tempo

ser=serial.Serial(argv[1],9600,timeout=5)
ser2=serial.Serial(argv[1],9600,timeout=5)
ser2.read()

if ser.isOpen():print "init [OK]"
else:
	print "init [NO]"
	exit(1)

fichier=open(argv[2])

ligne=fichier.readline()
while ligne!='':
	if ligne[0]=="T":
		tempo=int(ligne.split(" ")[1])
		longueur=tempo
	else:
		for i in range(0,len(NOTES)):
			t=ligne.strip().split(" ")
			#print t
			if t[0]==NOTES[i]:
				note=i
			if len(t)>1:
				octave=int(t[1])
			if len(t)>2:
				if "/" in t[2]:
					num,den=t[2].split("/")
					longueur=(tempo*int(num))/int(den)
				else:longueur=tempo*int(t[2])
		print NOTES[note],note,octave,longueur,
		joue(octave,note,longueur)
	ligne=fichier.readline()
fichier.close()
ser.close()
ser2.close()
