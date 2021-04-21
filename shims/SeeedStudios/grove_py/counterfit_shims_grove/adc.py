'''
This is the code for
    - `Grove Base Hat for RPi      <https://www.seeedstudio.com/Grove-WS2813-RGB-LED-Strip-Waterproof-60-LED-m-1m-p-3126.html>`_
    - `Grove Base Hat for RPi Zero <https://www.seeedstudio.com/Grove-Base-Hat-for-Raspberry-Pi-Zero-p-3187.html>`_

Grove Base Hat incorparates a micro controller STM32F030F4.

Raspberry Pi does not have ADC unit, so we use an external chip
to transmit analog data to raspberry pi.

Examples:
    .. code-block:: python

        import time
        from counterfit_connection import CounterFitConnection
        from counterfit_shims_grove.adc import ADC

        # Init the connection to the CounterFit Virtual IoT Device app
        CounterFitConnection.init('127.0.0.1', 5000)

        adc = ADC()
        while True:
            # Read channel 0(Slot A0)
            print(adc.read(0))
            time.sleep(1)

'''
# pylint: disable=no-self-use

# pylint: disable=import-error
from counterfit_connection import CounterFitConnection

__all__ = ["ADC"]

class ADC():
    '''
    Class ADC for the ADC unit on Grove Base Hat for RPi.

    Args:
        address(int): optional, i2c address of the ADC unit, default 0x04
    '''
    def __init__(self, address = 0x04):
        pass

    def read_raw(self, channel):
        '''
        Read the raw data of ADC unit, with 12 bits resolution.

        Args:
            channel (int): 0 - 7, specify the channel to read

        Returns:
            (int): the adc result, in [0 - 4095]
        '''
        raise NotImplementedError()

    # read input voltage (mV)
    def read_voltage(self, channel):
        '''
        Read the voltage data of ADC unit.

        Args:
            channel (int): 0 - 7, specify the channel to read

        Returns:
            (int): the voltage result, in mV
        '''
        raise NotImplementedError()

    # input voltage / output voltage (%)
    def read(self, channel):
        '''
        Read the ratio between channel input voltage and power voltage (most time it's 3.3V).

        Args:
            channel (int): 0 - 7, specify the channel to read

        Returns:
            (int): the ratio, in 0.1%
        '''
        return CounterFitConnection.get_sensor_int_value(channel)

    @property
    def name(self):
        '''
        Get the Hat name.

        Returns:
            (string): could be :class:`RPI_HAT_NAME` or :class:`RPI_ZERO_HAT_NAME`
        '''
        return 'Virtual Grove Hat'

    @property
    def version(self):
        '''
        Get the Hat firmware version.

        Returns:
            (int): firmware version
        '''
        return 1

    # pylint: disable=invalid-name
    def read_register(self, n):
        '''
        Read the ADC Core (through I2C) registers

        Grove Base Hat for RPI I2C Registers

            - 0x00 ~ 0x01: 
            - 0x10 ~ 0x17: ADC raw data
            - 0x20 ~ 0x27: input voltage
            - 0x29: output voltage (Grove power supply voltage)
            - 0x30 ~ 0x37: input voltage / output voltage

        Args:
            n(int): register address.

        Returns:
            (int) : 16-bit register value.
        '''
        raise NotImplementedError()
