'''
Tests the Grove light sensor shim.

To run this test, ensure you have the CounterFit Virtual IoT Device app running, with a light sensor
on pin 1 set to a value of 50

'''
# pylint: disable=redefined-outer-name,unused-argument

import pytest

from counterfit_connection import CounterFitConnection
from counterfit_shims_grove.grove_light_sensor_v1_2 import GroveLightSensor

@pytest.fixture
def init_counterfit_device():
    '''
    Test fixture to initialise the connection to the CounterFit Virtual IoT device running on localhost on port 5000
    '''
    CounterFitConnection.init('127.0.0.1', 5000)

def test_light_sensor_light_is_50(init_counterfit_device):
    '''
    Tests the light property of the Grove Light Sensor shim
    '''
    sensor = GroveLightSensor(0)
    assert sensor.light == 50
