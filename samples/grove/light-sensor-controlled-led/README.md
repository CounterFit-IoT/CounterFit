# Light sensor controlled LED sample

This sample shows how to use the CounterFit Grove shims to simulate an LED and a light sensor, controlling the LED based on the light levels read from the sensor.

## Setup

* Create a Python virtual environment:

    ```sh
    python3 -m venv .venv
    ```

* Activate the environment:

    macOS/Linux:

    ```sh
    source ./.venv/bin/activate
    ```

    Windows:

    ```cmd
    .venv\Scripts\activate.bat
    ```

* Install the required pip packages:

    ```sh
    pip install -r requirements.txt
    ```

This will install the [CounterFit](https://github.com/CounterFit-IoT/CounterFit/tree/main/counterfit-app) app and the [CounterFit Grove Shims](https://github.com/CounterFit-IoT/CounterFit/tree/main/shims/grove).

## Configure the hardware

* Launch the CounterFit app:

    ```sh
    CounterFit
    ```

    This will launch the app in a web browser, running on port 5000.

    > If you want to change the port, pass it is as the `--port` parameter when launching `CounterFit`

* Create a light sensor on pin 1, and an LED actuator on pin 2

## Run the code

* Run the `app.py` file in the same virtual environment (you will need a new terminal or CMD)

    > If you used a different port, then you will need to edit the port use to initialize the CounterFit connection:
    >
    > ```python
    > CounterFitConnection.init('127.0.0.1', <port>)
    > ```
    >
    > Replace `<port>` with the port you used.

* Adjust the values in CounterFit for the light level. When the value is less than 200, the LED will light up.
