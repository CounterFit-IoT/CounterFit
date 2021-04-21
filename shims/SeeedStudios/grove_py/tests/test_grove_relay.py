'''
Tests the Grove Relay shim.

To run this test, ensure you have the CounterFit Virtual IoT Device app running, with a relay actuator
on pin 1.

Uncomment the relevant test below and run it to see the relay change state

'''
# pylint: disable=redefined-outer-name,unused-argument

import pytest

from counterfit_connection import CounterFitConnection
from counterfit_shims_grove.grove_relay import GroveRelay

@pytest.fixture
def init_counterfit_device():
    '''
    Test fixture to initialise the connection to the CounterFit Virtual IoT device running on localhost on port 5000
    '''
    CounterFitConnection.init('127.0.0.1', 5000)

# def test_turn_relay_on(init_counterfit_device):
#     '''
#     Tests the on method of the Grove relay shim
#     '''
#     sensor = GroveRelay(1)
#     sensor.on()

def test_turn_relay_off(init_counterfit_device):
    '''
    Tests the off method of the Grove relay shim
    '''
    sensor = GroveRelay(1)
    sensor.off()
