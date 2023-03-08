# pylint: disable=protected-access,line-too-long
import datetime
import time

from CounterFit.serial_sensors import GPSSensor, GPSValueType


def test_decimal_degree_conversion():
    assert GPSSensor._decimal_decrees_to_ddmmm(47.653814) == "4739.22884"
    assert GPSSensor._decimal_decrees_to_ddmmm(-47.09565) == "4705.739"
    assert GPSSensor._decimal_decrees_to_ddmmm(-47) == "4700.0"


def test_checksum():
    assert (
        GPSSensor._build_checksum(
            "$GPGGA,005206.768,5227.561,N,01230.806,E,1,12,1.0,0.0,M,0.0,M,,*00"
        )
        == "68"
    )
    assert (
        GPSSensor._build_checksum(
            "GPGGA,005207.768,5249.958,N,01308.049,E,1,12,1.0,0.0,M,0.0,M,,*00"
        )
        == "6E"
    )
    assert (
        GPSSensor._build_checksum(
            "$GPGGA,005208.768,5310.190,N,01409.023,E,1,12,1.0,0.0,M,0.0,M,,*00"
        )
        == "6A"
    )
    assert (
        GPSSensor._build_checksum(
            "$GPGGA,005209.768,5300.094,N,01450.881,E,1,12,1.0,0.0,M,0.0,M,,*00"
        )
        == "63"
    )
    assert (
        GPSSensor._build_checksum(
            "$GPGGA,005210.768,5148.313,N,01608.005,E,1,12,1.0,0.0,M,0.0,M,,*00"
        )
        == "62"
    )
    assert (
        GPSSensor._build_checksum(
            "# $GPGGA,005211.768,5142.192,N,01454.836,E,1,12,1.0,0.0,M,0.0,M,,*00"
        )
        == "61"
    )
    assert (
        GPSSensor._build_checksum(
            "$GPGGA,005212.768,5135.443,N,01332.439,E,1,12,1.0,0.0,M,0.0,M,,*00"
        )
        == "6F"
    )
    assert (
        GPSSensor._build_checksum(
            "$GPGGA,005213.768,5153.810,N,01259.150,E,1,12,1.0,0.0,M,0.0,M,,*00"
        )
        == "62"
    )


def test_gps_empty_read_line():
    gps = GPSSensor("/dev/ttyAMA0")
    line = gps.read_line()
    assert line == ""


def test_gps_empty_read():
    gps = GPSSensor("/dev/ttyAMA0")
    char = gps.read()
    assert char == ""


def add_checksum_to_expected(expected: str) -> str:
    checksum = GPSSensor._build_checksum(expected)
    expected += checksum
    return expected


def test_gps_time_setting_when_using_lat_lon_n_e():
    gps = GPSSensor("/dev/ttyAMA0")
    gps.value_type = GPSValueType.LATLON

    gps.lat = 47
    gps.lon = 122
    gps.number_of_satellites = 3

    current_utc = datetime.datetime.utcnow()

    line = gps.read_line()

    expected = add_checksum_to_expected(
        f"$GPGGA,{current_utc.hour:02d}{current_utc.minute:02d}{current_utc.second:02}.00,4700.0,N,12200.0,E,1,3,,0,M,0,M,,*"
    )

    assert line == expected
    assert gps.read_line() == ""


def test_gps_time_setting_when_using_lat_lon_s_w():
    gps = GPSSensor("/dev/ttyAMA0")
    gps.value_type = GPSValueType.LATLON

    gps.lat = -47
    gps.lon = -122
    gps.number_of_satellites = 3

    current_utc = datetime.datetime.utcnow()

    expected = add_checksum_to_expected(
        f"$GPGGA,{current_utc.hour:02d}{current_utc.minute:02d}{current_utc.second:02}.00,4700.0,S,12200.0,W,1,3,,0,M,0,M,,*"
    )

    assert gps.read_line() == expected
    assert gps.read_line() == ""


def test_gps_nmea():
    gps = GPSSensor("/dev/ttyAMA0")
    gps.value_type = GPSValueType.NMEA

    gps.raw_nmea = (
        "$GNGGA,020604.001,4739.228833333,N,12207.031866667,W,1,3,,164.7,M,-17.1,M,,*67"
    )

    assert (
        gps.read_line()
        == "$GNGGA,020604.001,4739.228833333,N,12207.031866667,W,1,3,,164.7,M,-17.1,M,,*67"
    )
    assert gps.read_line() == ""


def test_gps_nmea_repeat():
    gps = GPSSensor("/dev/ttyAMA0")
    gps.value_type = GPSValueType.NMEA

    gps.raw_nmea = (
        "$GNGGA,020604.001,4739.228833333,N,12207.031866667,W,1,3,,164.7,M,-17.1,M,,*67"
    )
    gps.repeat = True

    for _ in range(0, 20):
        line = gps.read_line()
        if line == "":
            time.sleep(1)
            line = gps.read_line()

        assert (
            line
            == "$GNGGA,020604.001,4739.228833333,N,12207.031866667,W,1,3,,164.7,M,-17.1,M,,*67"
        )


def test_gps_nmea_repeat_has_delay():
    gps = GPSSensor("/dev/ttyAMA0")
    gps.value_type = GPSValueType.NMEA

    gps.raw_nmea = (
        "$GNGGA,020604.001,4739.228833333,N,12207.031866667,W,1,3,,164.7,M,-17.1,M,,*67"
    )
    gps.repeat = True

    line = gps.read_line()
    assert (
        line
        == "$GNGGA,020604.001,4739.228833333,N,12207.031866667,W,1,3,,164.7,M,-17.1,M,,*67"
    )

    line = gps.read_line()
    assert line == ""

    line = gps.read_line()
    assert line == ""

    line = gps.read_line()
    assert line == ""

    time.sleep(1)

    line = gps.read_line()
    assert (
        line
        == "$GNGGA,020604.001,4739.228833333,N,12207.031866667,W,1,3,,164.7,M,-17.1,M,,*67"
    )


def test_gps_nmea_multiple_sentences_has_delay():
    gps = GPSSensor("/dev/ttyAMA0")
    gps.value_type = GPSValueType.NMEA

    gps.raw_nmea = (
        "$GNGGA,020604.001,4739.228833333,N,12207.031866667,W,1,3,,164.7,M,-17.1,M,,*67"
        + "\n"
        + "$GNGGA,020604.001,4739.228833333,S,12207.031866667,E,1,3,,164.7,M,-17.1,M,,*67"
    )

    line = gps.read_line()
    assert (
        line
        == "$GNGGA,020604.001,4739.228833333,N,12207.031866667,W,1,3,,164.7,M,-17.1,M,,*67"
    )

    line = gps.read_line()
    assert line == ""

    line = gps.read_line()
    assert line == ""

    line = gps.read_line()
    assert line == ""

    time.sleep(1.5)

    line = gps.read_line()
    assert (
        line
        == "$GNGGA,020604.001,4739.228833333,S,12207.031866667,E,1,3,,164.7,M,-17.1,M,,*67"
    )


def test_gps_nmea_multiple_sentences_has_delay_only_for_gga():
    gps = GPSSensor("/dev/ttyAMA0")
    gps.value_type = GPSValueType.NMEA

    gps.raw_nmea = (
        "$GNGGA,020604.001,4739.228833333,N,12207.031866667,W,1,3,,164.7,M,-17.1,M,,*67"
        + "\n"
        + "$GPGSA,A,3,01,02,03,04,05,06,07,08,09,10,11,12,1.0,1.0,1.0*30"
        + "\n"
        + "$GNGGA,020604.001,4739.228833333,S,12207.031866667,E,1,3,,164.7,M,-17.1,M,,*67"
        + "\n"
        + "$GPGSA,A,3,01,02,03,04,05,06,07,08,09,10,11,12,1.0,1.0,1.0*30"
    )

    line = gps.read_line()
    assert (
        line
        == "$GNGGA,020604.001,4739.228833333,N,12207.031866667,W,1,3,,164.7,M,-17.1,M,,*67"
    )

    line = gps.read_line()
    assert line == "$GPGSA,A,3,01,02,03,04,05,06,07,08,09,10,11,12,1.0,1.0,1.0*30"

    line = gps.read_line()
    assert line == ""

    line = gps.read_line()
    assert line == ""

    time.sleep(1)

    line = gps.read_line()
    assert (
        line
        == "$GNGGA,020604.001,4739.228833333,S,12207.031866667,E,1,3,,164.7,M,-17.1,M,,*67"
    )

    line = gps.read_line()
    assert line == "$GPGSA,A,3,01,02,03,04,05,06,07,08,09,10,11,12,1.0,1.0,1.0*30"

    line = gps.read_line()
    assert line == ""

    line = gps.read_line()
    assert line == ""


def test_gps_gpx():
    gps = GPSSensor("/dev/ttyAMA0")
    gps.value_type = GPSValueType.GPX

    with open("./src/tests/route.gpx", "r", encoding="UTF-8") as gpx_file:
        gps.gpx_file_contents = gpx_file.read()

    current_utc = datetime.datetime.utcnow()
    assert gps.read_line() == add_checksum_to_expected(
        f"$GPGGA,{current_utc.hour:02d}{current_utc.minute:02d}{current_utc.second:02}.00,4744.0886,N,12215.42,W,1,3,,0,M,0,M,,*"
    )

    time.sleep(2)

    current_utc = datetime.datetime.utcnow()
    assert gps.read_line() == add_checksum_to_expected(
        f"$GPGGA,{current_utc.hour:02d}{current_utc.minute:02d}{current_utc.second:02}.00,4744.0886,N,12215.4206,W,1,3,,0,M,0,M,,*"
    )

    time.sleep(2)

    current_utc = datetime.datetime.utcnow()
    assert gps.read_line() == add_checksum_to_expected(
        f"$GPGGA,{current_utc.hour:02d}{current_utc.minute:02d}{current_utc.second:02}.00,4744.0856,N,12215.4092,W,1,3,,0,M,0,M,,*"
    )

    assert gps.read_line() == ""


def test_gps_gpx_repeat():
    gps = GPSSensor("/dev/ttyAMA0")
    gps.value_type = GPSValueType.GPX

    with open("./src/tests/route.gpx", "r", encoding="UTF-8") as gpx_file:
        gps.gpx_file_contents = gpx_file.read()

    gps.repeat = True

    for _ in range(0, 20):
        line = gps.read_line()
        if line == "":
            time.sleep(1)
            line = gps.read_line()

        current_utc = datetime.datetime.utcnow()
        assert line == add_checksum_to_expected(
            f"$GPGGA,{current_utc.hour:02d}{current_utc.minute:02d}{current_utc.second:02}.00,4744.0886,N,12215.42,W,1,3,,0,M,0,M,,*"
        )

        line = gps.read_line()
        if line == "":
            time.sleep(1)
            line = gps.read_line()

        current_utc = datetime.datetime.utcnow()
        assert line == add_checksum_to_expected(
            f"$GPGGA,{current_utc.hour:02d}{current_utc.minute:02d}{current_utc.second:02}.00,4744.0886,N,12215.4206,W,1,3,,0,M,0,M,,*"
        )

        line = gps.read_line()
        if line == "":
            time.sleep(1)
            line = gps.read_line()

        current_utc = datetime.datetime.utcnow()
        assert line == add_checksum_to_expected(
            f"$GPGGA,{current_utc.hour:02d}{current_utc.minute:02d}{current_utc.second:02}.00,4744.0856,N,12215.4092,W,1,3,,0,M,0,M,,*"
        )


def test_setting_lat_lon_clears_value():
    gps = GPSSensor("/dev/ttyAMA0")
    gps.value_type = GPSValueType.NMEA

    gps.raw_nmea = (
        "$GNGGA,020604.001,4739.228833333,N,12207.031866667,W,1,3,,164.7,M,-17.1,M,,*67"
    )

    gps.value_type = GPSValueType.LATLON

    gps.lat = -47
    gps.lon = -122
    gps.number_of_satellites = 3

    current_utc = datetime.datetime.utcnow()

    expected = add_checksum_to_expected(
        f"$GPGGA,{current_utc.hour:02d}{current_utc.minute:02d}{current_utc.second:02}.00,4700.0,S,12200.0,W,1,3,,0,M,0,M,,*"
    )

    assert gps.read_line() == expected
    assert gps.read_line() == ""


def test_setting_gpx_clears_value():
    gps = GPSSensor("/dev/ttyAMA0")
    gps.value_type = GPSValueType.NMEA

    gps.raw_nmea = (
        "$GNGGA,020604.001,4739.228833333,N,12207.031866667,W,1,3,,164.7,M,-17.1,M,,*67"
    )

    gps.value_type = GPSValueType.GPX

    with open("./src/tests/route.gpx", "r", encoding="UTF-8") as gpx_file:
        gps.gpx_file_contents = gpx_file.read()

    current_utc = datetime.datetime.utcnow()
    assert gps.read_line() == add_checksum_to_expected(
        f"$GPGGA,{current_utc.hour:02d}{current_utc.minute:02d}{current_utc.second:02}.00,4744.0886,N,12215.42,W,1,3,,0,M,0,M,,*"
    )

    time.sleep(2)

    current_utc = datetime.datetime.utcnow()
    assert gps.read_line() == add_checksum_to_expected(
        f"$GPGGA,{current_utc.hour:02d}{current_utc.minute:02d}{current_utc.second:02}.00,4744.0886,N,12215.4206,W,1,3,,0,M,0,M,,*"
    )

    time.sleep(2)

    current_utc = datetime.datetime.utcnow()
    assert gps.read_line() == add_checksum_to_expected(
        f"$GPGGA,{current_utc.hour:02d}{current_utc.minute:02d}{current_utc.second:02}.00,4744.0856,N,12215.4092,W,1,3,,0,M,0,M,,*"
    )

    assert gps.read_line() == ""


def test_setting_nmea_clears_value():
    gps = GPSSensor("/dev/ttyAMA0")

    gps.value_type = GPSValueType.GPX

    with open("./src/tests/route.gpx", "r", encoding="UTF-8") as gpx_file:
        gps.gpx_file_contents = gpx_file.read()

    gps.value_type = GPSValueType.NMEA

    gps.raw_nmea = (
        "$GNGGA,020604.001,4739.228833333,N,12207.031866667,W,1,3,,164.7,M,-17.1,M,,*67"
    )

    assert (
        gps.read_line()
        == "$GNGGA,020604.001,4739.228833333,N,12207.031866667,W,1,3,,164.7,M,-17.1,M,,*67"
    )
    assert gps.read_line() == ""
