from abc import abstractmethod
from enum import Enum
import datetime
import re
from bs4 import BeautifulSoup

from CounterFit.sensors import SensorBase, SensorType

class SerialSensorBase(SensorBase):
    def __init__(self, port:str):
        super().__init__(port)

        self.__value = ''
        self.__repeat = False
        self._next_repeat_time = None
        self._value_position = 0
    
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
        self._value_position = 0

    @property
    def repeat(self) -> bool:
        return self.__repeat

    @repeat.setter
    def repeat(self, val: bool):
        self.__repeat = val
    
    def read(self):
        current_utc = datetime.datetime.utcnow()
        if self._next_repeat_time is None:
            self._next_repeat_time = current_utc + datetime.timedelta(0, 1)

        if self._value_position >= len(self.value):
            if self.repeat and current_utc > self._next_repeat_time:
                self._next_repeat_time = current_utc
                self._value_position = 0
        
        if self._value_position >= len(self.value):
            return ''
        
        char = self.value[self._value_position]
        self._value_position += 1
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
        self.__substitute_value = ''
        self.__substitute_start_position = 0
        self.__substitute_end_position = 0
        self.__next_gpgga_line_time = None

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
    def _build_checksum(sentence:str) -> str:
        checksum_data = re.sub("(\n|\r\n)","", sentence[sentence.find("$")+1:sentence.find("*")])
        
        checksum = 0 
                
        for character in checksum_data:
            checksum ^= ord(character)
        
        return hex(checksum).replace('0x', '').upper().zfill(2)

    @staticmethod
    def _build_sentence_from_lat_lon_num_satellites(lat:float, lon:float, num_satellites:int) -> str:
        converted_lat = GPSSensor._decimal_decrees_to_ddmmm(lat)
        converted_lon = GPSSensor._decimal_decrees_to_ddmmm(lon)
        lat_dir = "N" if lat > 0 else "S"
        lon_dir = "E" if lon > 0 else "W"
        
        # use a timestamp of xxxxxx.xx, and this will be replaced with the current time when the value is requested
        # Use a checksum of zz, and again it will be replaces
        return f'$GPGGA,xxxxxx.xx,{converted_lat},{lat_dir},{converted_lon},{lon_dir},1,{num_satellites},,0,M,0,M,,*zz\n'

    def _build_value(self) -> None:
        if self.value_type == GPSValueType.LATLON:            
            self.value = GPSSensor._build_sentence_from_lat_lon_num_satellites(self.lat, self.lon, self.number_of_satellites)
        if self.value_type == GPSValueType.NMEA:
            self.value = self.raw_nmea
            if not self.value.endswith('\n'):
                self.value += '\n'
        if self.value_type == GPSValueType.GPX:
            self.value = ''
            soup = BeautifulSoup(self.gpx_file_contents, 'lxml')
            track_parts = soup.find_all('trkpt')
            for track_part in track_parts:
                self.value += GPSSensor._build_sentence_from_lat_lon_num_satellites(float(track_part['lat']), float(track_part['lon']), 3)
            
    def read(self):
        current_utc = datetime.datetime.utcnow()
        
        if self._next_repeat_time is None:
            self._next_repeat_time = current_utc + datetime.timedelta(0, 1)
            
        if self.__next_gpgga_line_time is None:
            self.__next_gpgga_line_time = current_utc + datetime.timedelta(0, 1)

        # only repeat after a delay
        if self._value_position >= len(self.value):
            if self.repeat and current_utc > self._next_repeat_time:
                self._next_repeat_time = current_utc + datetime.timedelta(0, 1)
                self._value_position = 0
        
        if self._value_position >= len(self.value):
            return ''

        chars_from_position = self.value[self._value_position:]

        # if we are a newline right before a $GPGGA then wait one second before sending it to space out GPX files or long NMEA data files
        if self._value_position > 0 and chars_from_position.startswith('$') and chars_from_position[3:].startswith('GGA'):
            if current_utc > self.__next_gpgga_line_time:
                self.__next_gpgga_line_time = current_utc + datetime.timedelta(0, 1)
            else:
                return ''

        if chars_from_position.startswith('$GPGGA,xxxxxx.xx'):
            self.__substitute_start_position = self._value_position

            # Find the end checksum
            self.__substitute_end_position = self.value.find('*zz', self._value_position) + len('*zz') 

            # find the block the right length
            self.__substitute_value = self.value[self.__substitute_start_position:self.__substitute_end_position]

            current_utc = datetime.datetime.utcnow()
            time_stamp = f'{current_utc.hour:02d}{current_utc.minute:02d}{current_utc.second:02}.00'
            self.__substitute_value = self.__substitute_value.replace('xxxxxx.xx', time_stamp)

            checksum = GPSSensor._build_checksum(self.__substitute_value)
            self.__substitute_value = self.__substitute_value.replace('*zz', '*' + checksum)

        if self.__substitute_start_position <= self._value_position and self.__substitute_end_position > self._value_position:
            next_char = self.__substitute_value[self._value_position - self.__substitute_start_position]
            self._value_position += 1
            return next_char
        
        self.__substitute_start_position = 0
        self.__substitute_end_position = 0
        self.__substitute_value = ''

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
