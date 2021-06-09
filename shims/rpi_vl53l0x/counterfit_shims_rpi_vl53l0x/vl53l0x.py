# pylint: disable=unused-argument,import-error
'''Shims for PySerial
'''

from counterfit_connection import CounterFitConnection

__all__ = ['VL53L0X']

class VL53L0X(object):
    def __init__(self, address:int = 0x29):
        self.__address = address

    def get_libver(self):
        return 'VL53L0X for CounterFit'

    def get_devver(self):
        return 'VL53L0X for CounterFit'

    def begin(self):
        return 0

    def wait_ready(self):
        '''
        return None  -- Error status
               False -- Timeout
               True  -- Ready
        '''
        return CounterFitConnection.is_connected()

    def get_distance(self):
        return CounterFitConnection.get_sensor_int_value(self.__address)