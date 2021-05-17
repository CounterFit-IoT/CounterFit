'''
Tests the PySerial connection.

To test this, launch CounterFit, and add 2 GPS sensors, one on /dev/tty0 and one on /dev/tty1.
Set them both to NMEA data, and the data as hello\nworld

'''
# pylint: disable=redefined-outer-name,unused-argument

import pytest

from counterfit_connection import CounterFitConnection
import counterfit_shims_serial

@pytest.fixture
def init_counterfit_device():
    '''
    Test fixture to initialise the connection to the CounterFit Virtual IoT device running on localhost on port 5000
    '''
    CounterFitConnection.init('127.0.0.1', 5000)

def test_read(init_counterfit_device):
    '''
    Tests values returned from the Serial port
    '''
    serial = counterfit_shims_serial.Serial('/dev/tty0')
    assert serial.read().decode('utf-8') == 'h'
    assert serial.read().decode('utf-8') == 'e'
    assert serial.read().decode('utf-8') == 'l'
    assert serial.read().decode('utf-8') == 'l'
    assert serial.read().decode('utf-8') == 'o'
    assert serial.read().decode('utf-8') == '\n'
    assert serial.read().decode('utf-8') == 'w'
    assert serial.read().decode('utf-8') == 'o'
    assert serial.read().decode('utf-8') == 'r'
    assert serial.read().decode('utf-8') == 'l'
    assert serial.read().decode('utf-8') == 'd'

def test_read_line(init_counterfit_device):
    '''
    Tests values returned from the Serial port
    '''
    serial = counterfit_shims_serial.Serial('/dev/tty1', 9600, timeout=1)
    assert serial.readline().decode('utf-8') == 'hello'
    assert serial.readline().decode('utf-8') == 'world'
