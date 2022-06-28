#from bluetooth import *
import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

# led settings
led_1 = 14
led_2 = 15
GPIO.setup(led_1, GPIO.OUT)
GPIO.setup(led_2, GPIO.OUT)
p1 = GPIO.PWM(led_1, 50)
p2 = GPIO.PWM(led_2, 50)

# piezo settings
GPIO.setmode(GPIO.BCM)
piezo = 13
GPIO.setup(piezo, GPIO.OUT)
scale = 500
p = GPIO.PWM(piezo, 100)

# bluetooth configuration
server = BluetoothSocket(RFCOMM)
server.bind(("", PORT_ANY))
server.listen(3)


def led_piezo():
    GPIO.output(led_1, False)
    GPIO.output(led_2, False)
    time.sleep(0.2)

    GPIO.output(led_1, True)
    GPIO.output(led_2, True)
    time.sleep(0.2)

    p.start(100)
    p.ChangeDutyCycle(100)
    p.ChangeFrequency(scale)
    time.sleep(0.2)

    Bluetooth()


def stop():
    p.stop()
    GPIO.output(led_1, False)
    GPIO.output(led_2, False)

#
# #def Bluetooth():
#     try:
#         client, info = server.accept()
#         print("connected")
#
#     except KeyboardInterrupt:
#         print("abort")
#         server.close()
#         exit()
#
#     fire_alarm = "FIRE!!!!! EVACUATE NOW!!!!!! OR YOU WILL BURN TO DEATH"
#     client.send(fire_alarm.encode())
