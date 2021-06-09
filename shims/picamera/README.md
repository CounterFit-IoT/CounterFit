# CounterFit Shims - Picamera

![Picamera Shim](https://img.shields.io/badge/Platform-Python-green) [![PyPI](https://img.shields.io/pypi/v/counterfit-shims-picamera)](https://pypi.org/project/counterfit-shims-picamera)

Shims for the Picamera to read from a virtual camera

See the [Picamera Docs](https://picamera.readthedocs.io/) for the API documentation.

## Getting started

To use these shims, you will need to install [CounterFit](https://github.com/CounterFit-IoT/CounterFit) and have it running, with the appropriate camera hardware created. Create the camera with a name of `Picamera`.

* Install this package from pip:

    ```sh
    pip install counterfit-shims-picamera
    ```

* Import Picamera using the `counterfit_shims_picamera` package instead of the `picamera` package, as well as importing the `CounterFitConnection` from the `counterfit_connection` module:

    ```python
    from counterfit_connection import CounterFitConnection
    import counterfit_shims_picamera
    ```

* Configure the connection to the CounterFit app. Change the hostname and port to where you are running it:

    ```python
    CounterFitConnection.init('127.0.0.1', 5000)
    ```

* Write your Picamers code as usual.

    For example, to capture an image as a JPEG:

    ```python
    camera = PiCamera()
    image = io.BytesIO()
    camera.capture(image, 'jpeg')
    ```
