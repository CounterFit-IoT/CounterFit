'''
This is the code for
    - `Grove - DHT11 digital temperature and humidity sensor <https://www.seeedstudio.com/Grove-Temperature-Humidity-Sensor-DHT11.html>`_

Examples:

    .. code-block:: python
        import time
        from counterfit_shims_seeed_python_dht.counterfit_connection import CounterFitConnection
        import counterfit_shims_seeed_python_dht.seeed_dht

        # Init the connection to the CounterFit Virtual IoT Device app
        CounterFitConnection.init('127.0.0.1', 5000)

        # connect to a humidity sensor on pin 12 and a temperature sensor on pin 13
        PIN   = 12
        sensor = seeed_dht.DHT("11", 12)

        humi, temp = sensor.read()
'''
# pylint: disable=too-few-public-methods,unused-argument

from counterfit_connection import CounterFitConnection

__all__ = ['DHT']

class DHT():
    '''
    Class for Grove DHT
    Args:
        pin(int): The pin for the humidity sensor. The temperature sensor needs to be on the next pin.
    '''
    def __init__(self, dht_type, pin = 12,bus_num = 1):
        self.__humidity_pin = pin
        self.__temperature_pin = pin + 1

    def read(self, retries = 15):
        '''
        Read the humidity and temperature from the sensor
        '''
        humidity = CounterFitConnection.get_sensor_float_value(self.__humidity_pin)
        temperature = CounterFitConnection.get_sensor_float_value(self.__temperature_pin)

        return humidity, temperature
