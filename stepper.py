import time
import RPi.GPIO as GPIO

class Stepper(object):
  """ Class used for stepper motor control """

  A1 = 22
  A2 = 27
  B1 = 23
  B2 = 24
  SLP = 18
  stepPins = [A1,A2,B1,B2]
  Seq3 = [[1,0,0,0],
          [0,0,1,0],
          [0,1,0,0],
          [0,0,0,1]]

  def __init__(self):
    GPIO.setmode(GPIO.BCM)
    # Set all pins as output
    GPIO.setup(Stepper.SLP, GPIO.OUT)
    GPIO.output(Stepper.SLP, True)
    for pin in Stepper.stepPins:
       GPIO.setup(pin,GPIO.OUT)
       GPIO.output(pin, False)

    self.stepCounter = 0
    self.waitTime = 0.01
    self.sequence = Stepper.Seq3

  def __enter__(self):
    return self

  def __exit__(self, ex_type, ex_value, traceback):
    self.close()

  def close(self):
    GPIO.cleanup(Stepper.SLP)
    for pin in Stepper.stepPins:
      GPIO.cleanup(pin)

  def step(self, forward=True):
    logicLevels = self.sequence[self.stepCounter]
    for i in range(0,len(logicLevels)):
      GPIO.output(Stepper.stepPins[i], logicLevels[i] == 1)
    
    direction = 1 if forward else -1
    self.stepCounter = (self.stepCounter + direction) % len(self.sequence)

  def stepForward(self, steps=1):
    for _ in range(steps):
      self.step(True)
      time.sleep(self.waitTime)

  def stepBackwards(self, steps=1):
    for _ in range(steps):
      self.step(False)
      time.sleep(self.waitTime)

  def setSpeed(self, stepsPerSecond):
    self.waitTime = 1. / stepsPerSecond

  def rotate(self, degrees):
    steps = int(degrees / 1.8)
    forward = degrees > 0
    for i in range(0,steps):
      self.step(forward)
      time.sleep(self.waitTime)