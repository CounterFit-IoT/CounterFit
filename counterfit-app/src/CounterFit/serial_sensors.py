from abc import abstractmethod
from enum import Enum
import datetime
from bs4 import BeautifulSoup

from CounterFit.sensors import SensorBase, SensorType

class SerialSensorBase(SensorBase):
    def __init__(self, port:str):
        super().__init__(port)

        self.__value = ''
        self.__repeat = False
        self.__repeat_value = ''
    
    @staticmethod
    def sensor_type() -> SensorType:
        return SensorType.SERIAL

    @staticmethod
    @abstractmethod
    def sensor_name() -> str:
        pass

    @property
    def id(self) -> str:
        return self.port.replace('/', '')

    @property
    def value(self) -> str:
        return self.__value

    @value.setter
    def value(self, val: str):
        self.__value = val

        if self.__repeat:
            self.__repeat_value = self.__value

    @property
    def repeat(self) -> bool:
        return self.__repeat

    @repeat.setter
    def repeat(self, val: bool):
        self.__repeat = val

        if self.__repeat:
            self.__repeat_value = self.__value
    
    def read(self):
        if len(self.value) == 0:
            if self.__repeat:
                self.value = self.__repeat_value

            if len(self.value) == 0:
                return ''
        
        char = self.value[0]
        self.value = self.value[1:]
        return char
    
    def read_line(self):        
        line = ''
        char = self.read()

        while char not in('\n', ''):            
            line = line + char
            char = self.read()
            
        return line

class GPSValueType(Enum):
    LATLON = 1
    NMEA = 2
    GPX = 3

class GPSSensor(SerialSensorBase):
    def __init__(self, port:str):
        super().__init__(port)
        self.__value_type = GPSValueType.LATLON
        self.__lat = 0.0
        self.__lon = 0.0
        self.__number_of_satellites = 0
        self.__raw_nmea = ''
        self.__gpx_file_name = ''
        self.__gpx_file_contents = ''

    @staticmethod
    def sensor_name() -> str:
        return 'UART GPS'

    @staticmethod
    def _decimal_decrees_to_ddmmm(decimal_degrees: float) -> str:
        decimal_degrees = abs(decimal_degrees)
        degrees = int(decimal_degrees)
        minutes = (float(decimal_degrees) - float(degrees)) * 60

        minutes_string = f'{minutes:.8f}'.zfill(11).rstrip('0')
        if minutes_string.endswith('.'):
            minutes_string += '0'

        return f'{degrees}{minutes_string}'

    @staticmethod
    def _build_sentence_from_lat_lon_num_satellites(lat:float, lon:float, num_satellites:int) -> str:
        converted_lat = GPSSensor._decimal_decrees_to_ddmmm(lat)
        converted_lon = GPSSensor._decimal_decrees_to_ddmmm(lon)
        lat_dir = "N" if lat > 0 else "S"
        lon_dir = "E" if lon > 0 else "W"
        
        # use a timestamp of xxxxxx.xxx, and this will be replaced with the current time when the value is requested
        return f'$GPGGA,xxxxxx.xxx,{converted_lat},{lat_dir},{converted_lon},{lon_dir},1,{num_satellites},,0,M,0,M,,0000'

    def _build_value(self) -> None:
        if self.value_type == GPSValueType.LATLON:            
            self.value = GPSSensor._build_sentence_from_lat_lon_num_satellites(self.lat, self.lon, self.number_of_satellites)
        if self.value_type == GPSValueType.NMEA:
            self.value = self.raw_nmea
        if self.value_type == GPSValueType.GPX:
            soup = BeautifulSoup(self.gpx_file_contents, 'lxml')
            track_parts = soup.find_all('trkpt')
            for track_part in track_parts:
                if len(self.value) > 0:
                    self.value += '\n'
                self.value += GPSSensor._build_sentence_from_lat_lon_num_satellites(float(track_part['lat']), float(track_part['lon']), 3)

    def read(self):
        # replace any time placeholders with the current UTC time
        if self.value.startswith('$GPGGA,xxxxxx.xxx'):
            current_utc = datetime.datetime.utcnow()
            time_str = f'{current_utc.hour:02d}{current_utc.minute:02d}{current_utc.second:02}.00'
            self.value = self.value.replace('xxxxxx.xxx', time_str, 1)
        return super().read()

    @property
    def value_type(self) -> GPSValueType:
        return self.__value_type

    @value_type.setter
    def value_type(self, val: GPSValueType):
        self.__value_type = val
        self._build_value()

    @property
    def lat(self) -> float:
        return self.__lat

    @lat.setter
    def lat(self, val: float):
        self.__lat = val
        self._build_value()

    @property
    def lon(self) -> float:
        return self.__lon

    @lon.setter
    def lon(self, val: float):
        self.__lon = val
        self._build_value()

    @property
    def number_of_satellites(self) -> int:
        return self.__number_of_satellites

    @number_of_satellites.setter
    def number_of_satellites(self, val: int):
        self.__number_of_satellites = val
        self._build_value()

    @property
    def raw_nmea(self) -> str:
        return self.__raw_nmea

    @raw_nmea.setter
    def raw_nmea(self, val: str):
        self.__raw_nmea = val
        self._build_value()

    @property
    def gpx_file_name(self) -> str:
        return self.__gpx_file_name

    @gpx_file_name.setter
    def gpx_file_name(self, val: str):
        self.__gpx_file_name = val
        self._build_value()

    @property
    def gpx_file_contents(self) -> str:
        return self.__gpx_file_contents

    @gpx_file_contents.setter
    def gpx_file_contents(self, val: str):
        self.__gpx_file_contents = val
        self._build_value()
