# pylint: disable=protected-access,line-too-long
import datetime

from CounterFit.serial_sensors import GPSSensor, GPSValueType

def test_decimal_degree_conversion():
    assert GPSSensor._decimal_decrees_to_ddmmm(47.653814) == '4739.22884'
    assert GPSSensor._decimal_decrees_to_ddmmm(-47.09565) == '4705.739'
    assert GPSSensor._decimal_decrees_to_ddmmm(-47) == '4700.0'

def test_gps_time_setting_when_using_lat_lon_n_e():
    gps = GPSSensor('/dev/ttyAMA0')
    gps.value_type = GPSValueType.LATLON

    gps.lat = 47
    gps.lon = 122
    gps.number_of_satellites = 3

    current_utc = datetime.datetime.utcnow()

    line = gps.read_line()

    assert line == f'$GPGGA,{current_utc.hour:02d}{current_utc.minute:02d}{current_utc.second:02}.00,4700.0,N,12200.0,E,1,3,,0,M,0,M,,0000'

def test_gps_time_setting_when_using_lat_lon_s_w():
    gps = GPSSensor('/dev/ttyAMA0')
    gps.value_type = GPSValueType.LATLON

    gps.lat = -47
    gps.lon = -122
    gps.number_of_satellites = 3

    current_utc = datetime.datetime.utcnow()

    assert gps.read_line() == f'$GPGGA,{current_utc.hour:02d}{current_utc.minute:02d}{current_utc.second:02}.00,4700.0,S,12200.0,W,1,3,,0,M,0,M,,0000'

def test_gps_nmea():
    gps = GPSSensor('/dev/ttyAMA0')
    gps.value_type = GPSValueType.NMEA

    gps.raw_nmea = '$GNGGA,020604.001,4739.228833333,N,12207.031866667,W,1,3,,164.7,M,-17.1,M,,*67' + \
                   '\n' + \
                   '$GNGGA,020604.001,4739.228833333,S,12207.031866667,E,1,3,,164.7,M,-17.1,M,,*67'

    assert gps.read_line() == '$GNGGA,020604.001,4739.228833333,N,12207.031866667,W,1,3,,164.7,M,-17.1,M,,*67'
    assert gps.read_line() == '$GNGGA,020604.001,4739.228833333,S,12207.031866667,E,1,3,,164.7,M,-17.1,M,,*67'

def test_gps_gpx():
    gps = GPSSensor('/dev/ttyAMA0')
    gps.value_type = GPSValueType.GPX

    with open('./src/tests/route.gpx', 'r') as gpx_file:
        gps.gpx_file_contents = gpx_file.read()
    
    current_utc = datetime.datetime.utcnow()

    assert gps.read_line() == f'$GPGGA,{current_utc.hour:02d}{current_utc.minute:02d}{current_utc.second:02}.00,4744.0886,N,12215.42,W,1,3,,0,M,0,M,,0000'
    assert gps.read_line() == f'$GPGGA,{current_utc.hour:02d}{current_utc.minute:02d}{current_utc.second:02}.00,4744.0886,N,12215.4206,W,1,3,,0,M,0,M,,0000'
    assert gps.read_line() == f'$GPGGA,{current_utc.hour:02d}{current_utc.minute:02d}{current_utc.second:02}.00,4744.0856,N,12215.4092,W,1,3,,0,M,0,M,,0000'
