# Relay controlled by temperature sensor and button sample

This sample shows how to use the CounterFit Grove shims to simulate a relay controlled by a temperature sensor and button setup.
The temperature value is read whenever the button is pressed, and the relay is activated if the temperature is under 38 degrees celcius.

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

This will install the [CounterFit](https://github.com/CounterFit-IoT/CounterFit/tree/main/counterfit-app) app and the [CounterFit Grove Shims](https://github.com/CounterFit-IoT/CounterFit/tree/main/shims).

## Configure the hardware

* Launch the CounterFit app:

    ```sh
    CounterFit
    ```

    This will launch the app in a web browser, running on port 5000.

    > If you want to change the port, pass it is as the `--port` parameter when launching `CounterFit`

* Create a **button** on **pin 1**, and a **temperature sensor** on **pin 2**, and a **relay** on **pin 3**
![Screenshot of the used setup](/assets/hardwareSetup.png)

## Run the code

* Run the `app.py` file in the same virtual environment (you will need a new terminal or CMD)

    > If you used a different port, then you will need to edit the port use to initialize the CounterFit connection:
    >
    > ```python
    > CounterFitConnection.init('127.0.0.1', <port>)
    > ```
    >
    > Replace `<port>` with the port you used.

* Adjust the values in CounterFit for the temperature level. When the value is less than 38 and the button is pressed, the relay will activate.