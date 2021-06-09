'''
Tests the RPI VL53L0X connection

Create a distance sensor at the address 0x29 and set teh distance to 100mm

'''
# pylint: disable=redefined-outer-name,unused-argument

import pytest

from counterfit_connection import CounterFitConnection
from counterfit_shims_rpi_vl53l0x.vl53l0x import VL53L0X

@pytest.fixture
def init_counterfit_device():
    '''
    Test fixture to initialise the connection to the CounterFit Virtual IoT device running on localhost on port 5000
    '''
    CounterFitConnection.init('127.0.0.1', 5000)

def test_get_distance(init_counterfit_device):
    '''
    Tests values returned from the Serial port
    '''
    distance_sensor = VL53L0X()
    distance_sensor.begin()

    if distance_sensor.wait_ready():
        assert distance_sensor.get_distance() == 100

