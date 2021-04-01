# CounterFit Shims - Grove

![Grove Shim](https://img.shields.io/badge/Platform-Python-green) [![PyPI](https://img.shields.io/pypi/v/counterfit-shims-grove)](https://pypi.org/project/counterfit-shims-grove)

Shims for the Seeed Grove sensors and actuators to use with the [CounterFit virtual IoT device app](https://github.com/CounterFit-IoT/CounterFit).

See the [Grove Py Docs](https://github.com/Seeed-Studio/grove.py) for the API documentation.

## Getting started

To use these shims, you will need to install [CounterFit](https://github.com/CounterFit-IoT/CounterFit) and have it running, with the appropriate hardware created.

* Install this package from pip:

    ```sh
    pip install counterfit-shims-grove
    ```

* Import the Grove modules as normal, but using the `counterfit_shims_grove` package instead of the `grove` package, as well as importing the `CounterFitConnection` from the `counterfit_shims_grove.counterfit_connection` module:

    ```python
    from counterfit_connection import CounterFitConnection
    from counterfit_shims_grove.grove_light_sensor_v1_2 import GroveLightSensor
    from counterfit_shims_grove.grove_led import GroveLed
    ```

* Configure the connection to the CounterFit app. Change the hostname and port to where you are running it:

    ```python
    CounterFitConnection.init('127.0.0.1', 5000)
    ```

* Write your Grove code as usual, setting the pins to match the ones you set in the CounterFit app:

    ```python
    light_sensor = GroveLightSensor(2)
    sensor_value = light_sensor.light
    ```

## Implemented shims

Not all the Grove sensor and actuators are currently implemented:

| Sensor/Actuator |
| ------ |
| grove_led |
| grove_light_sensor_v1_2 |
