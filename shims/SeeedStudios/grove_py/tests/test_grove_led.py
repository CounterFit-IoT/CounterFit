'''
Tests the Grove LED shim.

To run this test, ensure you have the CounterFit Virtual IoT Device app running, with an LED actuator
on pin 1.

Uncomment the relevant test below and run it to see the LED change state

'''
# pylint: disable=redefined-outer-name,unused-argument

import pytest

from counterfit_connection import CounterFitConnection
from counterfit_shims_grove.grove_led import GroveLed

@pytest.fixture
def init_counterfit_device():
    '''
    Test fixture to initialise the connection to the CounterFit Virtual IoT device running on localhost on port 5000
    '''
    CounterFitConnection.init('127.0.0.1', 5000)

def test_turn_led_on(init_counterfit_device):
    '''
    Tests the on method of the Grove LED shim
    '''
    sensor = GroveLed(1)
    sensor.on()

def test_turn_led_off(init_counterfit_device):
    '''
    Tests the off method of the Grove LED shim
    '''
    sensor = GroveLed(1)
    sensor.off()
