# CicruitPython
import pulseio
import array
import board
import time
import digitalio
import adafruit_irremote
from ElegooRemote import ElegooRemote

import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode

print("Starting...")

pulsein=pulseio.PulseIn(board.GP15,maxlen=120,idle_state=True)
decoder=adafruit_irremote.NonblockingGenericDecode(pulsein)
keyboard = Keyboard(usb_hid.devices)

boardLED = digitalio.DigitalInOut(board.GP25)
boardLED.direction = digitalio.Direction.OUTPUT

def process(value):
    print("processing")
    if value == ElegooRemote.FUNC:
        print("full screen toggle")
        keyboard.press(Keycode.F)
        time.sleep(0.1)
        keyboard.release(Keycode.F)
    elif value == ElegooRemote.PLAY:
        print("Playing/pause")
        keyboard.press(Keycode.SPACE)
        time.sleep(0.1)
        keyboard.release(Keycode.SPACE)
    elif value == ElegooRemote.FORWARD:
        print("forward")
        keyboard.press(Keycode.RIGHT_ARROW)
        time.sleep(0.1)
        keyboard.release(Keycode.RIGHT_ARROW)
    elif value == ElegooRemote.REVERSE:
        print("rewind")
        keyboard.press(Keycode.LEFT_ARROW)
        time.sleep(0.1)
        keyboard.release(Keycode.LEFT_ARROW) 
    elif value == ElegooRemote.VOLUP:
        print("Vol +")
        keyboard.press(Keycode.UP_ARROW)
        time.sleep(0.1)
        keyboard.release(Keycode.UP_ARROW)  
    elif value == ElegooRemote.VOLDOWN:
        print("Vol -")
        keyboard.press(Keycode.DOWN_ARROW)
        time.sleep(0.1) 
        keyboard.release(Keycode.DOWN_ARROW)
    # Alt tab : use to force screen to foreground
    elif value == ElegooRemote.EQ:
        print("Equal")
        keyboard.press(Keycode.ALT)
        time.sleep(0.1)
        keyboard.press(Keycode.TAB)
        time.sleep(0.1)
        keyboard.release(Keycode.TAB) 
        time.sleep(0.1)
        keyboard.release(Keycode.ALT)          
    else:      
      print("????")
    
time.sleep(2)
t0 = next_heartbeat = time.monotonic()
next_heartbeat_count=0
print("Started")

while True:
    try:
        for pulse in decoder.read():
            
            print("Heard", len(pulse.pulses), "Pulses:", pulse.pulses)
            boardLED.value = True
            
            if isinstance(pulse, adafruit_irremote.IRMessage):
                print("Decoded:", pulse.code)
                print("value: ", pulse.code[2])
                process(pulse.code[2])
                time.sleep(2)
            else:
                print("Issue decoding:", pulse.reason)
            
            print("-----------------")
    except:
        continue

    t=time.monotonic()
    if t> next_heartbeat: 
        next_heartbeat = t + 1 
        next_heartbeat_count += 1
        print("heartbeat")
        if(next_heartbeat_count % 5):
            boardLED.value = False
        else:
            # Only turn LED on for every 5th pulse
            boardLED.value = True
