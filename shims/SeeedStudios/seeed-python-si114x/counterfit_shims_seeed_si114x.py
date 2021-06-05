'''
This is the code for
    - `Grove - Sunlight sensor <https://www.seeedstudio.com/Grove-Sunlight-Sensor.html>`_

Examples:

    .. code-block:: python
        import time
        from counterfit_connection import CounterFitConnection
        import counterfit_shims_seeed_si114x

        # Init the connection to the CounterFit Virtual IoT Device app
        CounterFitConnection.init('127.0.0.1', 5000)

        light_sensor = seeed_si114x.grove_si114x()

        light = light_sensor.ReadVisible
'''
# pylint: disable=too-few-public-methods,unused-argument

from counterfit_connection import CounterFitConnection

__all__ = ['grove_si114x']

class grove_si114x():
    '''
    Class for Grove SI114X
    Args:
        light_pin(int): The pin for the light sensor
        ir_pin(int): The pin for the IR sensor
        uv_pin(int): The pin for the UV sensor
    '''
    def __init__(self, light_pin = 0, ir_pin = 1, uv_pin = 2):
        self.__light_pin = light_pin
        self.__ir_pin = ir_pin
        self.__uv_pin = uv_pin

    @property
    def ReadVisible(self):
        '''
        Read the visible light from the sensor
        '''
        return CounterFitConnection.get_sensor_int_value(self.__light_pin)

    @property
    def ReadIR(self):
        '''
        Read the IR light from the sensor
        '''
        return CounterFitConnection.get_sensor_int_value(self.__ir_pin)

    @property
    def ReadUV(self):
        '''
        Read the IR light from the sensor
        '''
        return CounterFitConnection.get_sensor_int_value(self.__uv_pin)
