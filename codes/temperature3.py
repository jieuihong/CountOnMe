import smbus
import time
import alert3

# import severe_alert

bus = smbus.SMBus(1)
addr = 0x40
cmd_temp = 0xf3
soft_reset = 0xfe
data = [0, 0]


def get_temp():
    bus.write_byte(addr, soft_reset)
    time.sleep(0.05)

    # get temperature
    bus.write_byte(addr, cmd_temp)
    time.sleep(0.260)

    temp = 0.0
    val = 0

    for i in range(0, 2, 1):
        data[i] = bus.read_byte(addr)
        val = data[0] << 8 | data[1]
    temp = -46.85 + 175.72 / 65536 * val

    time.sleep(1)

    return temp


def count_time():
    start_time = time.time()

    while True:
        if time.time() - start_time < 1:
            alert3.alert()
        else:
            break


while True:
    cur_temp = get_temp()
    print cur_temp

    if get_temp() > 26:
        count_time()
    else:
        alert3.stop()


