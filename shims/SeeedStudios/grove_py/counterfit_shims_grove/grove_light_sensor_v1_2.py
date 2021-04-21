'''
This is the shim code for
    - `Grove - Light Sensor <https://www.seeedstudio.com/Grove-Light-Sensor-v1.2-p-2727.html>`_

Examples:

    .. code-block:: python

        import time
        from counterfit_connection import CounterFitConnection
        from counterfit_shims_grove.grove_light_sensor_v1_2 import GroveLightSensor

        # Init the connection to the CounterFit Virtual IoT Device app
        CounterFitConnection.init('127.0.0.1', 5000)

        # connect to alalog pin 2(slot A2)
        PIN = 2

        sensor = GroveLightSensor(pin)

        print('Detecting light...')
        while True:
            print('Light value: {0}'.format(sensor.light))
            time.sleep(1)
'''
# pylint: disable=too-few-public-methods

# pylint: disable=import-error
from counterfit_connection import CounterFitConnection

__all__ = ['GroveLightSensor']

class GroveLightSensor:
    '''
    Grove Light Sensor class

    Args:
        pin(int): number of analog pin/channel the sensor connected.
    '''
    def __init__(self, pin: int):
        self.__pin = pin

    @property
    def light(self) -> int:
        '''
        Get the light strength value, maximum value is 1023
        '''
        return CounterFitConnection.get_sensor_int_value(self.__pin)
