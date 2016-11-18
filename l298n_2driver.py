#!/usr/bin/python2
#coding=utf-8
import RPi.GPIO as GPIO
import time
import pygame
from pygame.locals import *
import os,sys,tty,termios
import select
import termios
import tty

G_PIN_0 = 11    #IN1
G_PIN_1 = 12    #IN2
G_PIN_2 = 13    #ENA
G_PIN_3 = 15	#IN3
G_PIN_4 = 16 	#IN4
G_PIN_5 = 18	#ENB
G_PIN_6 = 22
G_PIN_7 = 7
VK_UP = 105   #i
VK_DOWN = 107 #k 
VK_LEFT = 106    #j	
VK_RIGHT = 108   #l

G_PIN_OUTLIST = [G_PIN_0,G_PIN_1,G_PIN_2,G_PIN_3,G_PIN_4,G_PIN_5]

#fd = sys.stdin.fileno()
#old_settings = termios.tcgetattr(fd)

def init():
#	pygame.init()
	GPIO.setmode(GPIO.BOARD)
	GPIO.setup(G_PIN_OUTLIST,GPIO.OUT)

def reset():
	GPIO.output(G_PIN_OUTLIST,GPIO.LOW)

def front_left_forward():
	GPIO.output(G_PIN_0,GPIO.HIGH)
	GPIO.output(G_PIN_1,GPIO.LOW)
	GPIO.output(G_PIN_2,GPIO.HIGH)

def front_left_backward():
	GPIO.output(G_PIN_0,GPIO.LOW)
	GPIO.output(G_PIN_1,GPIO.HIGH)
	GPIO.output(G_PIN_2,GPIO.HIGH)


def front_right_forward():
	GPIO.output(G_PIN_3,GPIO.HIGH)
	GPIO.output(G_PIN_4,GPIO.LOW)
	GPIO.output(G_PIN_5,GPIO.HIGH)

def front_right_backward():
        GPIO.output(G_PIN_3,GPIO.LOW)
        GPIO.output(G_PIN_4,GPIO.HIGH)
        GPIO.output(G_PIN_5,GPIO.HIGH)


def forward(t):
	print "forward"
	front_left_forward()
	front_right_forward()
	time.sleep(t)

def backward(t):
	print "backward"
	front_left_backward()
	front_right_backward()
	time.sleep(t)

def front_turn_left(t):
	print "left"
	front_left_backward()
	front_right_forward()
	time.sleep(t)

def front_turn_right(t):
	print "right"
	front_left_forward()
	front_right_backward()
	time.sleep(t)

def back_turn_left():
	front_left_forward()
	front_right_backward()

def back_turn_right():
	front_left_backward()
	front_right_forward()

def stop():
	reset()

movement_dict ={'i':forward,'k':backward,'j':front_turn_left,'l':front_turn_right}


def main():
	key_flag = False
	init()
	reset()
	'''time.sleep(1)
	print "forward\r\n"
	forward(1)
	time.sleep(1)
	print "backward\r\n"
	backward(1)
	time.sleep(1)
'''
	print "end\r\n"
	stop()
	ch = 0
	old_settings = termios.tcgetattr(sys.stdin)
	tty.setcbreak(sys.stdin.fileno())
	while True:
	    time.sleep(.001)
	    if select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], []):
	        c = sys.stdin.read(1)
		if key_flag == True :
			key_flag = False
	        if c == '\x04': break
		if c == '\x1b': 
			key_flag =True
		if c>= 'i' and c<= 'l':
			print "move"
			try :
				movement_dict[c](0.1)
			except Exception,e:
				print Exception,"::",e
				
	        sys.stdout.write(c)
	        sys.stdout.flush()
	termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
	
	GPIO.cleanup()
	'''while 1 :
		ch = sys.stdin.read(1)
		print "%s"%ch
		if 'Q'==ch:
			sys.exit()			
		if(0xe0==ch):
			ch=sys.stdin.read(1)
			movement.get(ch)(2)	
'''
	'''while True:
		pygame.display.flip()
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
			elif event.type ==KEYDOWN:
				key_flag = True
				keys = pygame.key.get_pressed()
				if keys ==K_LEFT:
					print "left"				
				if keys ==K_RIGHT:
					print "right"
				if keys == K_ESCAPE:
					print "es quit"
					pygame.quit()
					sys.exit()
			elif event.type == KEYUP:
				key_flag = False
	'''

if __name__ == "__main__":
	main()
