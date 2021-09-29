import RPi.GPIO as GPIO #import pythons rasberry pi library
from time import sleep #importing library so we can use sleep command
#need help? Text Nick or Rohith
GPIO.setmode(GPIO.BCM) #Set pin numbering mode to BCM rather than BOARD
#defining pin numbers
butt1, butt2, pinG, pinY, pinB=20,21,26,19,13


GPIO.setup(pinG, GPIO.OUT)          #The Green LED
my_pwm_green= GPIO.PWM(pinG, 1000)     # create PWM object at 1000Hz for smoothness
GPIO.setup(pinY, GPIO.OUT)          #The Yellow LED
my_pwm_yellow= GPIO.PWM(pinY, 1000)    # create PWM object at 1000Hz for smoothness
GPIO.setup(pinB, GPIO.OUT)          #the Blue LED that blinks on and off
GPIO.setup(butt1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) #The first Button
GPIO.setup(butt2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) #The second button

#defining the threaded callback function
def inputChange(pin):
  
  print("input pin ", pin ," status changed to: ", GPIO.input(pin) )

  if pin==butt2:
    my_pwm_yellow.start(0) #initiate the pwm object. starting it at 0% duty cycle
    for dc in range(0,101,1): # loop duty cycle, dc, from 0 to 100. 
      my_pwm_yellow.ChangeDutyCycle(dc) # set duty cycle
      sleep (0.005)                  # sleep 5 ms. 5ms*100 is half second. 
      print(dc)
    for dc in range(101,0,-1): #range(start,stop,step)
      print(dc)
      my_pwm_yellow.ChangeDutyCycle(dc-1)
      sleep(0.005) #half second ramp up, half second ramp down. 
    my_pwm_yellow.stop()
  elif pin==butt1:
    my_pwm_green.start(0) #initiate pwm object at 50% duty cycle
    for dc in range(0,101,1): # loop duty cycle, dc, from 0 to 100. 
      my_pwm_yellow.ChangeDutyCycle(dc) # set duty cycle
      sleep (0.005)                  # sleep 5 ms. 5ms*100 is half second. 
      print(dc)
    for dc in range(101,0,-1): #range(start,stop,step)
      print(dc)
      my_pwm_yellow.ChangeDutyCycle(dc-1)
      sleep(0.005) #half second ramp up, half second ramp down. 
    my_pwm_green.stop()




#checking for interrupt on the two button pins
GPIO.add_event_detect(butt1, GPIO.RISING, callback=inputChange, bouncetime=300) #debouncing =300
GPIO.add_event_detect(butt2, GPIO.RISING, callback=inputChange, bouncetime=300)

#the main loop that runs always. Blinking blue LED
try:
  while(True):
    GPIO.output(pinB,0)
    sleep(0.5)
    GPIO.output(pinB,1)
    sleep(0.5)
except KeyboardInterrupt: # if user hits ctrl-C
  print('\nExiting')
except Exception as e:    # catch all other errors
  print("\ne")

my_pwm_green.stop()
my_pwm_yellow.stop()
GPIO.cleanup()