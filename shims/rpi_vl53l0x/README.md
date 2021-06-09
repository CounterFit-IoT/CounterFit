# CounterFit Shims - PySerial

![PySerial Shim](https://img.shields.io/badge/Platform-Python-green) [![PyPI](https://img.shields.io/pypi/v/counterfit-shims-serial)](https://pypi.org/project/counterfit-shims-serial)

Shims for the PySerial to read sensors that use a virtual serial port

See the [PySerial Docs](https://pyserial.readthedocs.io/en/latest/pyserial.html) for the API documentation.

## Getting started

To use these shims, you will need to install [CounterFit](https://github.com/CounterFit-IoT/CounterFit) and have it running, with the appropriate hardware created.

* Install this package from pip:

    ```sh
    pip install counterfit-shims-serial
    ```

* Import PySerial using the `counterfit_shims_serial` package instead of the `serial` package, as well as importing the `CounterFitConnection` from the `counterfit_shims_grove.counterfit_connection` module:

    ```python
    from counterfit_connection import CounterFitConnection
    import counterfit_shims_serial
    ```

* Configure the connection to the CounterFit app. Change the hostname and port to where you are running it:

    ```python
    CounterFitConnection.init('127.0.0.1', 5000)
    ```

* Write your PySerial code as usual, setting the port to match the one you set in the CounterFit app.

    For example, create a UART sensor on port `/dev/ttyAMA0`:

    ```python
    serial = counterfit_shims_serial.Serial('/dev/ttyAMA0', 9600, timeout=1)
    ```

    The baud and timeout settings are ignored.
