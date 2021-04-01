'''
Tests the CounterFit app connection

To run this test, ensure you have the CounterFit Virtual IoT Device app running

'''
# pylint: disable=redefined-outer-name,unused-argument

import pytest

from counterfit_connection import CounterFitConnection

def test_init_counterfit_device():
    '''
    Tests the connection. You should see the CounterFit app status change to connected
    '''
    CounterFitConnection.init('127.0.0.1', 5000)
