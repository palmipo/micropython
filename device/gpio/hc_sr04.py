import rp2
import machine
import time

call HC_SR04:
  def __init__(self, trigger, echo):
    self.trigger_pin = Pin(trigger, 
