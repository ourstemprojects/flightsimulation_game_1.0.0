#!/usr/bin/python

import time
import random
import DebugLogger as d

BOARD = "board"
BCM = "bcm"
OUT = "out"
IN = "in"
RISING = "rising"
 
def output(pin,value):
  d.debug_print("testRPiGPIO.output(pin, value): pin=%s, value=%s" % (pin, value))
#endef

def input(pin):

  # wait a moment to simulate real-time nature of GPIO
  time.sleep(1)
  
  # get a random number 0..20 and if it is less than 10 return false otherwise return true
  value = random.randint(0, 20)
  if value <= 10:
    retval = False
  else:
    retval = True
  #endif

  # debug print pin and fake value
  d.debug_print("testRPiGPIO.input(pin): pin=%s; level=%d" % (pin, retval))

  # return the vale defined
  return retval
#enddef
 
def setmode(mode):
  d.debug_print("testRPiGPIO.setmode(mode): mode=%s" % (mode))
#endef
 
def setup(pin,value):
  d.debug_print("testRPiGPIO.setup(pin, value): pin=%s, value=%s" % (pin, value))
#endef  

def add_event_detect(pin, direction, callback):
  d.debug_print("testRPiGPIO.add_event_detect(pin, direction, callback): pin=%s, direction=%s, callback=%s" % (pin, direction, str(callback)))
#endef
 
def cleanup():
  d.debug_print("testRPiGPIO.cleanup():")
#endef
