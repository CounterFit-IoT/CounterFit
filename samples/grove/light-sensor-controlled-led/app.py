import time

from counterfit_connection import CounterFitConnection
from counterfit_shims_grove.grove_light_sensor_v1_2 import GroveLightSensor
from counterfit_shims_grove.grove_led import GroveLed

CounterFitConnection.init('127.0.0.1', 5000)

light_sensor = GroveLightSensor(1)
led = GroveLed(2)

while True:
    sensor_value = light_sensor.light
    print(f'Light sensor reading: {sensor_value}')

    if sensor_value > 200:
        print('Turning LED off')
        led.off()
    else:
        print('Turning LED on')
        led.on()

    time.sleep(2)