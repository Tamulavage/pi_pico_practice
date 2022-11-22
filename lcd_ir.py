#MicroPython
from machine import I2C, Pin
from time import sleep
from pico_i2c_lcd import I2cLcd

print("starting..")
i2c = I2C(0, sda=Pin(0),scl=Pin(1), freq=400000)
irScan = Pin(16, Pin.IN, Pin.PULL_DOWN)
buzzer = Pin(15, Pin.OUT, Pin.PULL_DOWN)

I2C_ADDR = i2c.scan()[0]
lcd= I2cLcd(i2c, I2C_ADDR,2,16)

lcd.blink_cursor_off()
lcd.backlight_off()
lcd.hide_cursor()
buzzer.value(0)
sleep(3)

print("Started")

while True:
    if irScan.value() == 1:
        print("Proximy Detected")
        
        lcd.backlight_on()
        lcd.putstr("Proximy Alert !!")
        
        for i in range(5,0,-1):
            lcd.move_to(0,1)
            lcd.putstr(str(i)+ " to alarm ! ")
            sleep(0.4)
            if irScan.value() == 0:
                break
            if i == 1:
                print("alarm sounding")
                lcd.clear()
                lcd.putstr("**** ALARM ***")
                lcd.move_to(0,1)
                lcd.putstr("** BACKUP NOW** ")
                
                while True:
                    buzzer.value(1)
                    sleep(0.1)    
                    if irScan.value() == 0:
                        buzzer.value(0)
                        break
                    
        lcd.clear()
        lcd.backlight_off()
    else:
        lcd.clear()
    sleep(.05)
    