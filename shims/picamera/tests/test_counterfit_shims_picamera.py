'''
Tests the PySerial connection.

To test this, launch CounterFit, and add 2 GPS sensors, one on /dev/tty0 and one on /dev/tty1.
Set them both to NMEA data, and the data as hello\nworld

'''
# pylint: disable=redefined-outer-name,unused-argument

import pytest

from counterfit_connection import CounterFitConnection
import counterfit_shims_picamera

@pytest.fixture
def init_counterfit_device():
    '''
    Test fixture to initialise the connection to the CounterFit Virtual IoT device running on localhost on port 5000
    '''
    CounterFitConnection.init('127.0.0.1', 5000)

def test_capture(init_counterfit_device):
    '''
    Tests capturing an image
    '''
    camera = counterfit_shims_picamera.PiCamera()
    camera.capture('test_image.png')
    camera.capture('test_image.jpeg')
    
def test_rotate(init_counterfit_device):
    '''
    Tests capturing an image
    '''
    camera = counterfit_shims_picamera.PiCamera()
    camera.rotation = 90
    camera.capture('test_image_rotate_90.jpeg')
    
    camera.rotation = 180
    camera.capture('test_image_rotate_180.jpeg')
    
    camera.rotation = 270
    camera.capture('test_image_rotate_270.jpeg')
    
def test_resolution_init(init_counterfit_device):
    '''
    Tests capturing an image
    '''
    camera = counterfit_shims_picamera.PiCamera((1024,768))
    camera.capture('test_image_resolution_1024_768_init.jpeg')
    
def test_resolution(init_counterfit_device):
    '''
    Tests capturing an image
    '''
    camera = counterfit_shims_picamera.PiCamera()
    camera.resolution = (1024,768)
    camera.capture('test_image_resolution_1024_768.jpeg')
    
def test_resolution_and_rotate(init_counterfit_device):
    '''
    Tests capturing an image
    '''
    camera = counterfit_shims_picamera.PiCamera()
    camera.rotation = 90
    camera.resolution = (1024,768)
    camera.capture('test_image_rotate_resolution_1024_768.jpeg')
