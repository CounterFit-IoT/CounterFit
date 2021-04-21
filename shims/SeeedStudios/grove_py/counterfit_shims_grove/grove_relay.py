'''
This is the code for
    - `Grove - Relay <https://www.seeedstudio.com/s/Grove-Relay-p-769.html>`_

Examples:

    .. code-block:: python

        import time
        from counterfit_connection import CounterFitConnection
        from counterfit_shims_grove.grove_relay import GroveRelay

        # Init the connection to the CounterFit Virtual IoT Device app
        CounterFitConnection.init('127.0.0.1', 5000)

        # connect to pin 5(slot D5)
        PIN   = 5
        relay = GroveRelay(PIN)

        while True:
            relay.on()
            time.sleep(1)
            relay.off()
            time.sleep(1)
'''

# pylint: disable=import-error
from counterfit_connection import CounterFitConnection

__all__ = ["GroveRelay"]

class GroveRelay():
    '''
    Class for Grove - Relay

    Args:
        pin(int): number of digital pin the relay connected.
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
