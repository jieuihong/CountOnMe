from bluetooth import *
import RPi.GPIO as GPIO
import time

# import severe_alert

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

# led settings
led_1 = 14
led_2 = 15
GPIO.setup(led_1, GPIO.OUT)
GPIO.setup(led_2, GPIO.OUT)

GPIO.output(led_1, False)
GPIO.output(led_2, False)

p1 = GPIO.PWM(led_1, 50)
p2 = GPIO.PWM(led_2, 50)

# piezo settings
GPIO.setmode(GPIO.BCM)
piezo = 13
GPIO.setup(piezo, GPIO.OUT)
scale = 392
p = GPIO.PWM(piezo, 100)

# bluetooth configuration
server = BluetoothSocket(RFCOMM)
server.bind(("", PORT_ANY))
server.listen(3)


def alert():
    GPIO.output(led_1, False)
    GPIO.output(led_2, False)
    time.sleep(0.4)

    p.start(100)
    p.ChangeDutyCycle(60)
    p.ChangeFrequency(scale)
    time.sleep(0.2)

    GPIO.output(led_1, True)
    GPIO.output(led_2, True)
    time.sleep(0.4)

    bluetooth()


def stop():
    p.stop()
    GPIO.output(led_1, False)
    GPIO.output(led_2, False)


def bluetooth():
    try:
        client, info = server.accept()
        print("connected")

    except KeyboardInterrupt:
        print("abort")
        server.close()
        exit()

    fire_alarm = "A fire has started in the building! Evacuate immediately!"
    client.send(fire_alarm.encode)
