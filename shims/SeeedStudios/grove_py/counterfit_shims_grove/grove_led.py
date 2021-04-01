'''
This is the code for
    - `Grove - Red LED    <https://www.seeedstudio.com/Grove-Red-LED-p-1142.html>`_
    - `Grove - Green LED  <https://www.seeedstudio.com/Grove-Green-LED-p-1144.html>`_
    - `Grove - Purple LED <https://www.seeedstudio.com/Grove-Purple-LED-3m-p-1143.html>`_
    - `Grove - White LED  <https://www.seeedstudio.com/Grove-White-LED-p-1140.html>`_

Examples:

    .. code-block:: python
        import time
        from counterfit_connection import CounterFitConnection
        from counterfit_shims_grove.grove_light_sensor_v1_2 import GroveLightSensor

        # Init the connection to the CounterFit Virtual IoT Device app
        CounterFitConnection.init('127.0.0.1', 5000)

        # connect to pin 5(slot D5)
        PIN   = 5
        led = GroveLed(PIN)
        while True:
            led.on()
            time.sleep(1)
            led.off()
            time.sleep(1)
'''

from counterfit_connection import CounterFitConnection

__all__ = ['GroveLed']

class GroveLed():
    '''
    Class for Grove - XXXX Led
    Args:
        pin(int): number of digital pin the led connected.
    '''
    def __init__(self, pin):
        self.__pin = pin

    # pylint: disable=invalid-name
    def on(self) -> None:
        '''
        light on the led
        '''
        CounterFitConnection.set_actuator_boolean_value(self.__pin, True)

    def off(self) -> None:
        '''
        light off the led
        '''
        CounterFitConnection.set_actuator_boolean_value(self.__pin, False)
