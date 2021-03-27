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
    def get_sensor_float_value(pin: int) -> float:
        '''
        Reads a float value from the sensor on the given pin
        '''
        response = requests.get(CounterFitConnection.base_url + 'sensor_value?pin=' + str(pin))
        return float(response.json()['value'])
    
    @staticmethod
    def get_sensor_int_value(pin: int) -> int:
        '''
        Reads an integer value from the sensor on the given pin
        '''
        response = requests.get(CounterFitConnection.base_url + 'sensor_value?pin=' + str(pin))
        return int(response.json()['value'])
    
    @staticmethod
    def get_sensor_boolean_value(pin: int) -> bool:
        '''
        Reads a bool value from the sensor on the given pin
        '''
        response = requests.get(CounterFitConnection.base_url + 'sensor_value?pin=' + str(pin))
        return bool(response.json()['value'])
    
    @staticmethod
    def set_actuator_float_value(pin: int, value: float) -> None:
        '''
        Sends a float value to the actuator on the given pin
        '''
        requests.post(CounterFitConnection.base_url + 'actuator_value?pin=' + str(pin), json= {'value':value})
    
    @staticmethod
    def set_actuator_boolean_value(pin: int, value: bool) -> None:
        '''
        Sends a bool value to the actuator on the given pin
        '''
        requests.post(CounterFitConnection.base_url + 'actuator_value?pin=' + str(pin), json= {'value':value})
