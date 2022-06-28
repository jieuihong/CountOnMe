import time
import RPi.GPIO as GPIO
from temperature import Temperature
import alert
#from bluetooth import *

GPIO.setmode(GPIO.BCM)
GPIO_TRIGGER = 0
GPIO_ECHO = 1

# trigger pin - output mode / echo pin - input mode
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# bluetooth configuration
#server = BluetoothSocket(RFCOMM)
#server.bind(("", PORT_ANY))
#server.listen(3)

d_first = 0
d_second = 0
inside = 0


def distance():
    while True:
        GPIO.output(GPIO_TRIGGER, True)
        time.sleep(0.00001)
        GPIO.output(GPIO_TRIGGER, False)
        StartTime = time.time()
        StopTime = time.time()

        # starting time - when echo pin turns off
        while GPIO.input(GPIO_ECHO) == 1:
            StartTime = time.time()

        # bounce time - when echo pin turns on
        while GPIO.input(GPIO_ECHO) == 0:
            StopTime = time.time()

        TimeElapsed = StopTime - StartTime
        distance = (TimeElapsed * 34300) / 2

        if distance > 200:
            continue
        else:
            return distance


def in_or_out(d_first, d_second, en, ex):
    if (10 <= d_first < 20) and (1 <= d_second < 10):
        en += 1
        print('entered')
    elif (10 <= d_second < 20) and (1 <= d_first < 10):
        ex += 1
        print('exited')
    else:
        pass
    return en - ex
    # print("number of people inside:", inside)


# try:
#     print 'test1'
#     time.sleep(10)
#     client, info = server.accept()
#     print 'test2'
#
# except KeyboardInterrupt:
#     server.close()
#     exit()


# def text_alert(inside):
#     # try:
#     #     client, info = server.accept()
#     #
#     # except KeyboardInterrupt:
#     #     server.close()
#     #     exit()
#
#     num_of_ppl = "The number of people inside: " + str(inside)
#     client.send(num_of_ppl.encode())
#
#
# def evacuated():
#     # try:
#     #     client, info = server.accept()
#     #
#     # except KeyboardInterrupt:
#     #     server.close()
#     #     exit()
#
#     evacuate = "Everyone in the building has evacuated"
#     client.send(evacuate.encode())


# if __name__ == '__main__':
entered = 0
exited = 0

# bluetooth configuration
# print 'test1'
# server = BluetoothSocket(RFCOMM)
# server.bind(("", PORT_ANY))
# server.listen(3)

#try:
#    client, info = server.accept()
#    print 'test2'
#except KeyboardInterrupt:
#    print("abort")
#    server.close()
#    exit()

try:
    while True:
        # first bounce the object makes
        d_first = distance()
        print("First Distance = %.1f cm" % d_first)
        time.sleep(2)

        # second bounce the object makes
        d_second = distance()
        print("Second Distance = %.1f cm" % d_second)

        # figure out whether the object entered or exited
        inside += in_or_out(d_first, d_second, entered, exited)
        print('inside:', inside)

        # alert.text_alert(inside)

        temperature = Temperature()
        temperature.get_temp()
        # if status<
        if temperature.fire_start:
            if inside == 0:
                #alert.evacuated()
                print("Everyone in the building has evacuated")
                alert.stop()

except KeyboardInterrupt:
    GPIO.cleanup()
