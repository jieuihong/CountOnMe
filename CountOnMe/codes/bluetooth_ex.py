from bluetooth import *
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
piezo= 13
GPIO.setup(piezo, GPIO.OUT)
scale = 392
p = GPIO.PWM(piezo, 100)

server = BluetoothSocket(RFCOMM)
server.bind(("", PORT_ANY))
server.listen(3)


def dual_fading():
    p1.start(0)
    p2.start(0)
    for dc in range(0, 101, 5):
        p1.ChangeDutyCycle(100-dc)
        p2.ChangeDutyCycle(dc)
        time.sleep(0.1)
    for dc in range(100, -1, -5):
        p1.ChangeDutyCycle(100-dc)
        p2.ChangeDutyCycle(dc)
        time.sleep(0.1)


def invasion():
    while True:
        if GPIO.input(pir) == True:
            invade = "Invasion Detected"
            print(invade)
            client.send(invade.encode())
            p.start(50)
            time.sleep(1)
        p.stop()
        time.sleep(1)
        safe = "safe"
        print(safe)
        client.send(safe.encode())


print("start server... ")

try:
    client, info = server.accept()
    print("client mac: ", info[0], ", port: ", info[1])

except KeyboardInterrupt:
    print("abort")
    server.close()
    exit()

try:
    while True:
        byte_data = client.recv(1024)
        data = byte_data.decode().strip()
        print("received: ", data)

        if "quit" in data:
            print("good bye")
            GPIO.cleanup()
            break

        elif data == "1":
            forward()
            backwards()
            one = "one"
            print(one)
            client.send(one.encode())

        elif data == "2":
            dual_fading()
            two = "two"
            print(two)
            client.send(two.encode())

        elif data == "3":
            invasion()

        client.send(data.encode())

except KeyboardInterrupt:
    print("terminate")
finally:
    GPIO.cleanup()
