#!/usr/bin/python

import time
import random

BOARD = "board"
BCM = "bcm"
OUT = "out"
IN = "in"
RISING = "rising"
 
def output(pin,value):
  print "testRPiGPIO.output(pin, value): pin=%s, value=%s" % (pin, value)
#endef

def input(pin):
  print "testRPiGPIO.input(pin): pin=%s" % (pin)
  time.sleep(random.randint(1, 5))
  return False
#enddef
 
def setmode(mode):
  print "testRPiGPIO.setmode(mode): mode=%s" % (mode)
#endef
 
def setup(pin,value):
  print "testRPiGPIO.setup(pin, value): pin=%s, value=%s" % (pin, value)
#endef  

def add_event_detect(pin, direction, callback):
  print "testRPiGPIO.add_event_detect(pin, direction, callback): pin=%s, direction=%s, callback=%s" % (pin, direction, str(callback))
#endef
 
def cleanup():
  print "testRPiGPIO.cleanup():"
#endef
