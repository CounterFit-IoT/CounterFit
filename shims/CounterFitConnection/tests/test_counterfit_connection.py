'''
Tests the CounterFit app connection

To run this test, ensure you have the CounterFit Virtual IoT Device app running

'''
# pylint: disable=redefined-outer-name,unused-argument,duplicate-code

import pytest
import time

from counterfit_connection import CounterFitConnection

def test_init_counterfit_device():
    '''
    Tests the connection. You should see the CounterFit app status change to connected
    '''
    CounterFitConnection.init('127.0.0.1', 5000)

# def test_get_sensor_bool_value():
#     '''
#     Tests reading a True boolean value from a boolean sensor on port 0
#     '''
#     CounterFitConnection.init('127.0.0.1', 5000)
#     assert CounterFitConnection.get_sensor_boolean_value(0)

# def test_read_serial_char():
#     '''
#     Tests reading a character from a serial sensor on port /dev/ttyAMA0 containing the text 'hello'
#     '''
#     CounterFitConnection.init('127.0.0.1', 5000)
#     assert CounterFitConnection.read_serial_sensor_char('/dev/ttyAMA0') == 'h'
#     assert CounterFitConnection.read_serial_sensor_char('/dev/ttyAMA0') == 'e'
#     assert CounterFitConnection.read_serial_sensor_char('/dev/ttyAMA0') == 'l'
#     assert CounterFitConnection.read_serial_sensor_char('/dev/ttyAMA0') == 'l'
#     assert CounterFitConnection.read_serial_sensor_char('/dev/ttyAMA0') == 'o'

# def test_read_serial_line():
#     '''
#     Tests reading a line from a serial sensor on port /dev/ttyAMA0 containing the text 'hello\nworld'
#     '''
#     CounterFitConnection.init('127.0.0.1', 5000)
#     assert CounterFitConnection.read_serial_sensor_line('/dev/ttyAMA0') == 'hello'
#     assert CounterFitConnection.read_serial_sensor_line('/dev/ttyAMA0') == 'world'

def test_camera_image():
    '''
    Tests reading an image from a camera sensor. The image is saved locally
    '''
    CounterFitConnection.init('127.0.0.1', 5000)
    image_data = CounterFitConnection.read_binary_sensor('Picamera')

    with open('test_image.png', 'wb') as image_file:
        image_file.write(image_data.read())

def test_is_connected():
    '''
    Tests is connected. Make sure counterfit is running
    '''
    CounterFitConnection.init('127.0.0.1', 5000)
    assert CounterFitConnection.is_connected()

def test_is_connected_is_false():
    '''
    Tests is connected. Make sure counterfit is running until you see a message telling you to close it
    '''
    CounterFitConnection.init('127.0.0.1', 5000)
    print("Please close counterfit")
    time.sleep(10)
    assert not CounterFitConnection.is_connected()
