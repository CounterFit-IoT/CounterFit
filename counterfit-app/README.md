# CounterFit

IoT is great fun, but has a downside - hardware. You need access to a range of devices such as sensors and actuators to build your IoT projects. Sometimes you might have these devices, other times you may not - maybe you are waiting for a delivery, or parts are out of stock, or they are too expensive.

That's where this tool comes in.

## What is CounterFit

CounterFit is a tool that is designed to fake various IoT hardware components, such as LEDs, buttons, temperature sensors and the like, that you can then access from IoT device code running on your computer rather than on an IoT device. It is made of two parts:

* The CounterFit app - this is a web app run locally where you can connect fake sensors and actuators to your virtual hardware
* Shims - these are libraries that mimic popular hardware APIs so you can take code that runs against well known hardware and run it against the CounterFit app.

## Getting started

* Install the CounterFit app:

    ```sh
    pip install CounterFit
    ```

* Run the app:

    ```sh
    CounterFit
    ```

* The app will launch, listening for web requests on port 5000, and open a web browser for you to start adding virtual sensors and actuators to your project

### Running on a different port

To use a different port than the default 5000, set the `--port` option when you run the app:

```sh
CounterFit --port 5050
```

## Connecting your code

You can connect your device code to CounterFit, using one of the available shims. See the [shim list for more details](https://github.com/CounterFit-IoT/CounterFit#shims).
