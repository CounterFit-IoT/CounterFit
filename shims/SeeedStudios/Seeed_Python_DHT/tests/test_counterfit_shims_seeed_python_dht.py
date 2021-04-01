'''
Tests the Grove DHT.

To run this test, ensure you have the CounterFit Virtual IoT Device app running, with a humidity sensor
on pin 0 and a temperature sensor on pin 1.

The humidity sensor should be set to 50%, and the temperature sensor to 25°C

'''
# pylint: disable=redefined-outer-name,unused-argument

import pytest

from counterfit_connection import CounterFitConnection
from counterfit_shims_seeed_python_dht import DHT

@pytest.fixture
def init_counterfit_device():
    '''
    Test fixture to initialise the connection to the CounterFit Virtual IoT device running on localhost on port 5000
    '''
    CounterFitConnection.init('127.0.0.1', 5000)

def test_humidity_and_temperature(init_counterfit_device):
    '''
    Tests values returned from the DHT sensor
    '''
    sensor = DHT("11", 12)

    humi, temp = sensor.read()


    assert humi == 50.0
    assert temp == 25.0
