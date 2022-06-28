import RPi.GPIO as GPIO
import time
from bluetooth import *

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

#led configuration
led1=14
led2=15
pwm_pin=13

GPIO_out=[led1,led2,pwm_pin]
GPIO.setup(GPIO_out,GPIO.OUT)
#GPIO.setup(pir,GPIO.IN)

server = BluetoothSocket(RFCOMM)
server.bind(("", PORT_ANY))
server.listen(3)
print("start server...")

p1=GPIO.PWM(led1,70)
p2=GPIO.PWM(led2,70)
p1.start(0)
p2.start(0)
p = GPIO.PWM(pwm_pin, 100)


try:
    client, info = server.accept()
    print("client mac:", info[0], ", port:", info[1])
except KeyboardInterrupt:
    server.close()
    exit()

def dual():
        print('LED fading effect!')
        #client.send('LED fading effect!'.encode())
        for dc in range(0, 101, 5):
            p1.ChangeDutyCycle(dc)
            p2.ChangeDutyCycle(100 - dc)
            time.sleep(0.03)

        for dc in range(0, 101, 5):
            p1.ChangeDutyCycle(100 - dc)
            p2.ChangeDutyCycle(dc)
            time.sleep(0.03)

def sensor():
        p.start(100)
        p.ChangeDutyCycle(90)
        p.ChangeFrequency(261)
        time.sleep(1)
        #p.stop()

        print("Intruders!")
        #client.send('Intruders!'.encode())
        GPIO.output(led1, True)
        time.sleep(0.8)

   # elif (count==0):
   #     print("Now in safe!")
   #     #client.send('Now in safe!'.encode())
   #
   #     time.sleep(0.8)

try:
    while True:
        #data = client.recv(1024)
        count=int(input("count="))
        sensor(count)
        dual(count)

#
#
except KeyboardInterrupt:
    print("terminate")
# client.close()
# server.close()
