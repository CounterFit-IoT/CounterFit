

# In this example:
# We will create a circuit where, when a button is pressed, we will check the current temperature
# If the recorded temperature is under 38 celsius, the relay will be activated


# PIN 1: Button
# PIN 2: Temperature sensor
# PIN 3: Relay

import time

from counterfit_connection import CounterFitConnection
from counterfit_shims_grove.grove_relay import GroveRelay

CounterFitConnection.init('127.0.0.1', 5000)

relay = GroveRelay(3)

while True:
    
    button = CounterFitConnection.get_sensor_boolean_value(1) # The button returns boolean values, True for pressed and False for released

    if button:
        print("The button has been pressed")
        temperature = CounterFitConnection.get_sensor_float_value(2) # Get temperature value

        print(f"Recorded temperature is {temperature}")

        if temperature < 38:
            print("Activate relay")
            relay.on()
            time.sleep(5)
            relay.off()

    time.sleep(0.5) # Used a short sleep timer as not to miss a button press when the script is on break
