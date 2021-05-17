# pylint: disable=C0103,E0401,W0603

import argparse
import json
import webbrowser
from threading import Timer
from flask import Flask, request, render_template
from flask_socketio import SocketIO

from CounterFit.sensors import SensorBase, SensorType
from CounterFit.serial_sensors import GPSSensor, GPSValueType, SerialSensorBase
from CounterFit.actuators import ActuatorBase

app = Flask(__name__)
app.config['SECRET_KEY'] = '247783f3-bdda-4536-bffc-109e2464f10b'
socketio = SocketIO(app)

sensor_cache = {}
actuator_cache = {}

all_sensors = []
all_actuators = []

is_connected = False

def get_all_subclasses(cls, class_list):
    for sub_class in cls.__subclasses__():
        if len(sub_class.__abstractmethods__) == 0:
            class_list.append(sub_class)

        get_all_subclasses(sub_class, class_list)

get_all_subclasses(SensorBase, all_sensors)
get_all_subclasses(ActuatorBase, all_actuators)

all_sensors = sorted(all_sensors, key=lambda s: s.sensor_name())
all_actuators = sorted(all_actuators, key=lambda a: a.actuator_name())

@app.route('/', methods=['GET'])
def home():
    ports = []
    for port in range(0, 26):
        str_port = str(port)
        if str_port not in sensor_cache and str_port not in actuator_cache:
            ports.append(str_port)

    return render_template('home.html', 
                           sensors=sensor_cache.values(),
                           actuators=actuator_cache.values(), 
                           all_sensors=all_sensors,
                           all_actuators=all_actuators,
                           is_connected = is_connected,
                           ports=ports)

def set_and_send_connected(connected:bool = True) -> None:
    global is_connected
    is_connected = connected
    socketio.emit('device_connect', {'connected' : is_connected})

@app.route('/connect', methods=['POST'])
def device_connect():
    set_and_send_connected()

    return 'OK', 200

@app.route('/disconnect', methods=['POST'])
def device_disconnect():
    set_and_send_connected(False)

    return 'OK', 200

def create_pin_sensor(sensor, body):
    port = str(body['pin'])
    unit = body['unit']

    if sensor.sensor_type() == SensorType.FLOAT:
        new_sensor = sensor(port, unit)
    elif sensor.sensor_type() == SensorType.INTEGER:
        new_sensor = sensor(port, unit)
    else:
        new_sensor = sensor(port)

    sensor_cache[port] = new_sensor

def create_serial_sensor(sensor, body):
    port = body['port']
    new_sensor = sensor(port)
    sensor_cache[port] = new_sensor

@app.route('/create_sensor', methods=['POST'])
def create_sensor():
    body = request.get_json()

    print('Create sensor called:', body)
    
    sensor_type = body['type']

    for sensor in all_sensors:
        if sensor.sensor_name() == sensor_type:
            if sensor.sensor_type() == SensorType.SERIAL:
                create_serial_sensor(sensor, body)
            else:
                create_pin_sensor(sensor, body)

    return 'OK', 200

@app.route('/create_actuator', methods=['POST'])
def create_actuator():
    body = request.get_json()

    print('Create actuator called:', body)
    
    actuator_type = body['type']
    port = body['port']

    for actuator in all_actuators:
        if actuator.actuator_name() == actuator_type:
            new_actuator = actuator(port)

            actuator_cache[port] = new_actuator

    return 'OK', 200

@app.route('/sensor_value', methods=['GET'])
def get_sensor_value():
    set_and_send_connected()
    port = str(request.args.get('port', ''))
    if port in sensor_cache:
        sensor = sensor_cache[port]
        
        response = {'value' : sensor.value}
        print('Returning sensor value', response, 'for port', port)

        return json.dumps(response)
    
    return 'Sensor with port ' + str(port) + ' not found', 404

@app.route('/serial_sensor_character', methods=['GET'])
def get_serial_sensor_character():
    set_and_send_connected()
    port = str(request.args.get('port', ''))
    if port in sensor_cache:
        sensor: SerialSensorBase = sensor_cache[port]
        
        response = {'value' : sensor.read()}
        print('Returning sensor value', response, 'for port', port)

        return json.dumps(response)
    
    return 'Sensor with port ' + str(port) + ' not found', 404

@app.route('/serial_sensor_line', methods=['GET'])
def get_serial_sensor_line():
    set_and_send_connected()
    port = str(request.args.get('port', ''))
    if port in sensor_cache:
        sensor: SerialSensorBase = sensor_cache[port]
        
        response = {'value' : sensor.read_line()}
        print('Returning sensor value', response, 'for port', port)

        return json.dumps(response)
    
    return 'Sensor with port ' + str(port) + ' not found', 404

@app.route('/delete_sensor', methods=['POST'])
def delete_sensor():
    body = request.get_json()

    print('Delete sensor called:', body)

    port = body['port']

    if port in sensor_cache:
        del sensor_cache[port]

    return 'OK', 200

@app.route('/delete_actuator', methods=['POST'])
def delete_actuator():
    body = request.get_json()

    print('Delete actuator called:', body)

    port = body['port']

    if port in actuator_cache:
        del actuator_cache[port]

    return 'OK', 200

@app.route('/float_sensor_settings', methods=['POST'])
def set_float_sensor_settings():
    body = request.get_json()

    print('Float sensor settings called:', body)
    
    port = body['port']
    value = body['value']
    is_random = body['is_random']
    random_min = body['random_min']
    random_max = body['random_max']

    if port in sensor_cache:
        sensor = sensor_cache[port]
        sensor.value = value
        sensor.random = is_random
        sensor.random_min = random_min
        sensor.random_max = random_max

    return 'OK', 200

@app.route('/integer_sensor_settings', methods=['POST'])
def set_integer_sensor_settings():
    body = request.get_json()

    print('Integer sensor settings called:', body)
    
    port = body['port']
    value = body['value']
    is_random = body['is_random']
    random_min = body['random_min']
    random_max = body['random_max']

    if port in sensor_cache:
        sensor = sensor_cache[port]
        sensor.value = value
        sensor.random = is_random
        sensor.random_min = random_min
        sensor.random_max = random_max

    return 'OK', 200

@app.route('/led_actuator_settings', methods=['POST'])
def set_led_actuator_settings():
    body = request.get_json()

    print('LED actuator settings called:', body)
    
    port = body['port']
    color = body['color']

    if port in actuator_cache:
        actuator = actuator_cache[port]
        actuator.color = color

    return 'OK', 200

@app.route('/boolean_sensor_settings', methods=['POST'])
def set_boolean_sensor_settings():
    body = request.get_json()

    print('Boolean sensor settings called:', body)
    
    port = body['port']
    value = body['value']
    is_random = body['is_random']

    if port in sensor_cache:
        sensor = sensor_cache[port]
        sensor.value = value
        sensor.random = is_random

    return 'OK', 200

@app.route('/gps_sensor_settings', methods=['POST'])
def set_gps_sensor_settings():
    body = request.get_json()
    
    print('GPS sensor settings called:', body)

    port = body['port']

    if port in sensor_cache:
        sensor : GPSSensor = sensor_cache[port]
        sensor.repeat = body['repeat']
        source = body['source']

        if source == 'latlon':
            sensor.value_type = GPSValueType.LATLON
            sensor.lat = body['lat']
            sensor.lon = body['lon']
            sensor.number_of_satellites = body['number_of_satellites']
        elif source == 'nmeasentences':
            sensor.value_type = GPSValueType.NMEA
            sensor.raw_nmea = body['nmea']
        else:
            sensor.value_type = GPSValueType.GPX
            sensor.gpx_file_contents = body['gpx']
            sensor.gpx_file_name = body['gpx_file_name']

    return 'OK', 200

@app.route('/sensor_units', methods=['POST'])
def get_sensor_units():
    body = request.get_json()

    print('Sensor units called:', body)

    sensor_type = body['type']

    #pylint: disable=R1705
    for sensor in all_sensors:
        if sensor.sensor_name() == sensor_type:
            if sensor.sensor_type() == SensorType.FLOAT:
                return {'units':sensor.sensor_units()}
            elif sensor.sensor_type() == SensorType.INTEGER:
                return {'units':sensor.sensor_units()}
            else:
                return {'units':[]}

    return 'Not found', 404

@app.route('/actuator_value', methods=['POST'])
def set_actuator_value():
    set_and_send_connected()
    port = str(request.args.get('port', ''))
    body = request.get_json()

    print('Actuator value called:', body, 'for port', port)

    value = body['value']

    if port in actuator_cache:
        actuator = actuator_cache[port]
        actuator.value = value

        socketio.emit('actuator_change' + str(port), {'port':port, 'value': value})

    return 'OK', 200

def open_browser(port):
    webbrowser.open_new(f'http://127.0.0.1:{port}/')

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', metavar='port', type=int, default=5000, help='the port to run on')

    args = parser.parse_args()

    print(f'CounterFit - virtual IoT hardware running on port {args.port}')

    Timer(3, open_browser, [args.port]).start()
    
    socketio.run(app, port=args.port)

if __name__ == '__main__':
    main()
