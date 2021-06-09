'''
Provides a connection to the CounterFit Virtual IoT Device app. This connection is re-used by all the virtual sensors.

Examples:

    When connecting to localhost on the default port:

    .. code-block:: python

        from counterfit_shims_grove.counterfit_connection import CounterFitConnection

        CounterFitConnection.init()


    When connection to another computer on a different port:

    .. code-block:: python

        from counterfit_shims_grove.counterfit_connection import CounterFitConnection

        CounterFitConnection.init('192.168.197.1', 5050)
'''
# pylint: disable=duplicate-code,bare-except

from base64 import b64decode
import io
import requests

class CounterFitConnection:
    '''
    Connects to the CounterFit Virtual IoT device on a give host and port, and allows the value of sensors to be read,
    as well as setting the value of actuators.
    '''
    base_url = ''

    @staticmethod
    def init(hostname: str = 'localhost', port: int = 5000) -> None:
        '''
        Initializes the connection to the Virtual IoT Device running on the given url and port
        '''
        CounterFitConnection.base_url = f'http://{hostname}:{str(port)}/'
        requests.post(CounterFitConnection.base_url + 'connect')
    
    @staticmethod
    def get_sensor_float_value(port: int) -> float:
        '''
        Reads a float value from the sensor on the given port
        '''
        response = requests.get(CounterFitConnection.base_url + 'sensor_value?port=' + str(port))
        return float(response.json()['value'])
    
    @staticmethod
    def get_sensor_int_value(port: int) -> int:
        '''
        Reads an integer value from the sensor on the given port
        '''
        response = requests.get(CounterFitConnection.base_url + 'sensor_value?port=' + str(port))
        return int(response.json()['value'])
    
    @staticmethod
    def get_sensor_boolean_value(port: int) -> bool:
        '''
        Reads a bool value from the sensor on the given port
        '''
        response = requests.get(CounterFitConnection.base_url + 'sensor_value?port=' + str(port))
        return bool(response.json()['value'])
    
    @staticmethod
    def read_serial_sensor_char(port: str) -> str:
        '''
        Reads a character from the serial sensor on the given port
        '''
        response = requests.get(CounterFitConnection.base_url + 'serial_sensor_character?port=' + port)
        return str(response.json()['value'])
    
    @staticmethod
    def read_serial_sensor_line(port: str) -> str:
        '''
        Reads a line from the serial sensor on the given port
        '''
        response = requests.get(CounterFitConnection.base_url + 'serial_sensor_line?port=' + port)
        return str(response.json()['value'])
    
    @staticmethod
    def read_binary_sensor(port: str) -> io.BytesIO:
        '''
        Reads a character from the serial sensor on the given port
        '''
        response = requests.get(CounterFitConnection.base_url + 'binary_sensor_data?port=' + port)
        msg = b64decode(response.json()['value'])
        return io.BytesIO(msg)
    
    @staticmethod
    def set_actuator_float_value(port: int, value: float) -> None:
        '''
        Sends a float value to the actuator on the given port
        '''
        requests.post(CounterFitConnection.base_url + 'actuator_value?port=' + str(port), json= {'value':value})
    
    @staticmethod
    def set_actuator_boolean_value(port: int, value: bool) -> None:
        '''
        Sends a bool value to the actuator on the given port
        '''
        requests.post(CounterFitConnection.base_url + 'actuator_value?port=' + str(port), json= {'value':value})
    
    @staticmethod
    def is_connected() -> bool:
        '''
        Determines if CounterFit is running
        '''
        try:
            requests.post(CounterFitConnection.base_url + 'connect')
            return True
        except:
            return False
