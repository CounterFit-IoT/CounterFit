'''
Tests the Grove SI114X.

To run this test, ensure you have the CounterFit Virtual IoT Device app running, with a light sensor
on pin 0, a IR sensor on pin 1, and a UV sensor on pin 2.

The light sensor should be set to 500, the IR sensor to 750, and the UV sensor to 1000

'''
# pylint: disable=redefined-outer-name,unused-argument

import pytest

from counterfit_connection import CounterFitConnection
from counterfit_shims_seeed_si114x import grove_si114x

@pytest.fixture
def init_counterfit_device():
    '''
    Test fixture to initialise the connection to the CounterFit Virtual IoT device running on localhost on port 5000
    '''
    CounterFitConnection.init('127.0.0.1', 5000)

def test_humidity_and_temperature(init_counterfit_device):
    '''
    Tests values returned from the SI114X sensor
    '''
    sensor = grove_si114x()

    assert sensor.ReadVisible == 500
    assert sensor.ReadIR == 750
    assert sensor.ReadUV == 1000
