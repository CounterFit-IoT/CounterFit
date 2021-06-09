# CounterFit Shims - VL53L0X distance sensor

![RPI_VL53L0X Shim](https://img.shields.io/badge/Platform-Python-green) [![PyPI](https://img.shields.io/pypi/v/counterfit-shims-rpi-vl53l0x)](https://pypi.org/project/counterfit-shims-rpi-vl53l0x)

Shims for the Rpi-VL53L0X distance sensor.

See the [Rpi-VL53L0X Docs](https://github.com/turmary/VL53L0X_rasp) for the API documentation.

## Getting started

To use these shims, you will need to install [CounterFit](https://github.com/CounterFit-IoT/CounterFit) and have it running, with the appropriate hardware created.

* Install this package from pip:

    ```sh
    pip install counterfit-shims-rpi-vl53l0x
    ```

* Import VL53L0X using the `counterfit_shims_rpi-vl53l0x` package instead of the `rpi-vl53l0x` package, as well as importing the `CounterFitConnection` from the `counterfit_connection` module:

    ```python
    from counterfit_connection import CounterFitConnection
    from counterfit_shims_rpi_vl53l0x.vl53l0x import VL53L0X
    ```

* Configure the connection to the CounterFit app. Change the hostname and port to where you are running it:

    ```python
    CounterFitConnection.init('127.0.0.1', 5000)
    ```

* Write your VL53L0X code as usual, setting the I<sup>2</sup>C address to match the one you set in the CounterFit app.

    For example, create a distance sensor on port `0x29`:

    ```python
    distance_sensor = VL53L0X(0x29)
    ```

