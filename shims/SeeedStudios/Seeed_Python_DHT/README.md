# CounterFit Shims - Grove

![Grove Shim](https://img.shields.io/badge/Platform-Python-green) [![PyPI](https://img.shields.io/pypi/v/counterfit-shims-seeed-python-dht)](https://pypi.org/project/counterfit-shims-seeed-python-dht)

Shims for the Seeed Grove DHT digital temperature and humidity sensor to use with the [CounterFit virtual IoT device app](https://github.com/CounterFit-IoT/CounterFit).

See the [Seeed Python DHT Docs](https://github.com/Seeed-Studio/Seeed_Python_DHT) for the API documentation.

## Getting started

To use these shims, you will need to install [CounterFit](https://github.com/CounterFit-IoT/CounterFit) and have it running, with the appropriate hardware created.

* Install this package from pip:

    ```sh
    pip install counterfit-shims-seeed-python-dht
    ```

* Import the Grove modules as normal, but using the `counterfit_shims_seeed_python_dht` package instead of the `seeed-python-dht` package, as well as importing the `CounterFitConnection` from the `counterfit_shims_grove.counterfit_connection` module:

    ```python
    from counterfit_connection import CounterFitConnection
    from counterfit_shims_seeed_python_dht import DHT
    ```

* Configure the connection to the CounterFit app. Change the hostname and port to where you are running it:

    ```python
    CounterFitConnection.init('127.0.0.1', 5000)
    ```

* Write your Grove code as usual, setting the pins to match the ones you set in the CounterFit app. To keep to the interface that the `DHT` specifies, only one pin can be passed to the constructor. The sensor assumes the pin given is for the humidity sensor, and the temperature is on the next pin.

    For example, create a humidity sensor on pin 1, and a temperature sensor on pin 2. Then pass 1 to the `DHT` constructor.

    ```python
    sensor =.DHT("11", 1)
    humi, temp = sensor.read()
    ```
