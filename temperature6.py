import smbus
import time
import alert
import severe_alert

class Temperature:
    def __init__(self):
        self.bus = smbus.SMBus(1)
        self.addr = 0x40

        self.cmd_temp = 0xf3
        self.soft_reset = 0xfe
        self.temp = 0.0
        self.val = 0
        self.data = [0, 0]
        self.fire_time = 0
        self.fire_start = 0


    def get_temp(self):
        self.bus.write_byte(self.addr, self.soft_reset)
        time.sleep(0.05)

        # get temperature
        self.bus.write_byte(self.addr, self.cmd_temp)
        time.sleep(0.260)
        for i in range(0, 2, 1):
            self.data[i] = self.bus.read_byte(self.addr)
        val = self.data[0] << 8 | self.data[1]
        temp = -46.85 + 175.72 / 65536 * val

        if temp > 29:
            self.fire_start = 1
            self.fire_time += 1
            self.count_time()
        elif temp <= 29:
            alert.stop()

        print 'temp: %.2f' % temp
        return self.fire_start


    def count_time(self):
        start_time = time.time()
        while True:
            if time.time() - start_time < 1:
                alert.led_piezo()
            if self.fire_time > 10:
                severe_alert.led_piezo()
            #elif 10 < time.time() - start_time < 20:
            #    severe_alert.led_piezo()
            else:
                break

