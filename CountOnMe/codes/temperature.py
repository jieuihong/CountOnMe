import smbus
import time
import alert
import threading
#import severe_alert

bus = smbus.SMBus(1)
addr = 0x40

cmd_temp = 0xf3
soft_reset = 0xfe
temp = 0.0
val = 0
data = [0, 0]


def get_temp():
    bus.write_byte(addr, soft_reset)
    time.sleep(0.05)

    # get temperature
    bus.write_byte(addr, cmd_temp)
    time.sleep(0.260)
    for i in range(0, 2, 1):
        data[i] = bus.read_byte(addr)
    val = data[0] << 8 | data[1]
    temp = -46.85 + 175.72 / 65536 * val

    if temp > 28:
        start_time = time.time()
        print('This is start time: ', str(start_time))
        count_time(start_time)
        time.sleep(1)

    print('temp: %.2f, before return get_temp' % temp)
    return temp


def count_time(start_time):
    while True:
        if time.time() - start_time < 1:
            alert.led_piezo()
            th_alarm = threading.Thread(target=alert.led_piezo)

            th_alarm.start()
        else:
            break
            # severe_alert.alarm()
            # severe_alert.dual_fading()
            # severe_alert.bluetooth()


try:
    th_temp = threading.Thread(target=get_temp)
    get_temp()
except KeyboardInterrupt:
    pass


