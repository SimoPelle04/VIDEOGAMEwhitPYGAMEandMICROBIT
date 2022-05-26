from microbit import *
import music


while True:
    b = False
    a = accelerometer.get_x()
    c = compass.heading()
    if button_a.is_pressed():
        b = True
        music.play(music.BA_DING)
    
    print (a,c,b)
    sleep(100)
    