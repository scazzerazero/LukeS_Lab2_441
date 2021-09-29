import RPi.GPIO as GPIO #import pythons rasberry pi library
from time import sleep #importing library so we can use sleep command
GPIO.setmode(GPIO.BCM) #Set pin numbering mode to BCM rather than BOARD
butt1, butt2, pinG, pinY, pinB=21,20,26,19,13 #defining pin numbers


GPIO.setup(pinG, GPIO.OUT)          #The Green LED
my_pwm_green= GPIO.PWM(pinG, 1000)  #Create PWM object at 1000Hz for smoothness
GPIO.setup(pinY, GPIO.OUT)          #The Yellow LED
my_pwm_yellow= GPIO.PWM(pinY, 1000)    
GPIO.setup(pinB, GPIO.OUT)          
GPIO.setup(butt1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) #The first Button. Yell LED
GPIO.setup(butt2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) #The second button. Gree LED

#defining the threaded callback function. Green or Yellow 1Hz Triangle wave.
def inputChange(pin):
  print("input pin ", pin ," status changed to: ", GPIO.input(pin) )
  if pin==butt1:# If button one is pressed initiate green triangle wave
    my_pwm_green.start(0) #initiate pwm object at 50% duty cycle
    for dc in range(0,101,1): # loop duty cycle, dc, from 0 to 100. 
      my_pwm_green.ChangeDutyCycle(dc) # set duty cycle
      sleep (0.005)                  # sleep 5 ms. 5ms*100 is half second. 
    for dc in range(101,0,-1): #range(start,stop,step)
      my_pwm_green.ChangeDutyCycle(dc-1)
      sleep(0.005) #half second ramp up, half second ramp down. 
    my_pwm_green.stop()
  elif pin==butt2: # If button two is pressed initiate yellow triangle wave
    my_pwm_yellow.start(0) 
    for dc in range(0,101,1): 
      my_pwm_yellow.ChangeDutyCycle(dc) 
      sleep (0.005)                  
    for dc in range(101,0,-1): 
      my_pwm_yellow.ChangeDutyCycle(dc-1)
      sleep(0.005) 
    my_pwm_yellow.stop()


#checking for interrupt on the two button pins. #debouncing =300
GPIO.add_event_detect(butt1, GPIO.RISING, callback=inputChange, bouncetime=300) 
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

GPIO.cleanup()