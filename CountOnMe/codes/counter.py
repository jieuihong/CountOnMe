import temperature

while True:
    curr_temp = temperature.get_temp()
    print('temp: %.2f' % curr_temp)

    if curr_temp > 30:
        count_time()
