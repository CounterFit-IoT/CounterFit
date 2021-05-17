# pylint: disable=unused-argument,import-error
'''Shims for PySerial
'''

from counterfit_connection import CounterFitConnection

__all__ = ['Serial']

class Serial():
    '''Shims for the PySerial Serial class
    '''
    def __init__(self, port: str, baud: int, **kwargs):
        self.__port = port

    def read(self, **kwargs) -> str:
        '''Reads a character from the serial port
        '''
        return CounterFitConnection.read_serial_sensor_char(self.__port)

    def readline(self, **kwargs) -> str:
        '''Reads a line from the serial port
        '''
        return CounterFitConnection.read_serial_sensor_line(self.__port)

    def reset_input_buffer(self):
        '''Does nothing - here for PySerial compatability
        '''

    def flush(self):
        '''Does nothing - here for PySerial compatability
        '''
