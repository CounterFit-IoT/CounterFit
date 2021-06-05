# CounterFit Shims - Grove

![Grove Shim](https://img.shields.io/badge/Platform-Python-green) [![PyPI](https://img.shields.io/pypi/v/counterfit-shims-seeed-python-si114x)](https://pypi.org/project/counterfit-shims-seeed-python-si114x)

Shims for the Seeed Grove SI114X sunlight sensor to use with the [CounterFit virtual IoT device app](https://github.com/CounterFit-IoT/CounterFit).

See the [Seeed Python SI114X Docs](https://github.com/Seeed-Studio/Seeed_Python_SI114X) for the API documentation.

## Getting started

To use these shims, you will need to install [CounterFit](https://github.com/CounterFit-IoT/CounterFit) and have it running, with the appropriate hardware created.

* Install this package from pip:

    ```sh
    pip install counterfit-shims-seeed-python-si114x
    ```

* Import the Grove modules as normal, but using the `counterfit_shims_seeed_python_si114x` package instead of the `seeed-python-si114x` package, as well as importing the `CounterFitConnection` from the `counterfit_shims_grove.counterfit_connection` module:

    ```python
    from counterfit_connection import CounterFitConnection
    from counterfit_shims_seeed_python_si114x import si114x
    ```

* Configure the connection to the CounterFit app. Change the hostname and port to where you are running it:

    ```python
    CounterFitConnection.init('127.0.0.1', 5000)
    ```

* Write your Grove code as usual. The default assumes you hve a light sensor on pin 0, IR on pin 1 and UV on pin 2. You can change these passing additional arguments to the init

    ```python
    sensor =.si114x()
    light = sensor.ReadVisible()
    ir = sensor.ReadIR()
    uv = sensor.ReadUV()
    ```
