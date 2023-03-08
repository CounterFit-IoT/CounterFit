from abc import abstractmethod
from enum import Enum
import io

from CounterFit.sensors import SensorBase, SensorType


class BinarySensorBase(SensorBase):
    def __init__(self, name: str):
        super().__init__(name)
        self.__value = io.BytesIO()
        self._next_repeat_time = None
        self._value_position = 0

    @staticmethod
    def sensor_type() -> SensorType:
        return SensorType.BINARY

    @staticmethod
    @abstractmethod
    def sensor_name() -> str:
        pass

    @property
    def id(self) -> str:
        return self.port.replace("/", "").replace(" ", "")

    @property
    def value(self) -> io.BytesIO:
        return self.__value

    @value.setter
    def value(self, val: io.BytesIO):
        self.__value = val


class CameraImageSource(Enum):
    FILE = 1
    WEBCAM = 2


class CameraSensor(BinarySensorBase):
    def __init__(self, name: str):
        super().__init__(name)
        self.__image_source = CameraImageSource.FILE
        self.__image_file_name = ""
        self.__web_cam_device_id = ""

    @staticmethod
    def sensor_name() -> str:
        return "Camera"

    @property
    def image_source(self) -> CameraImageSource:
        return self.__image_source

    @image_source.setter
    def image_source(self, val: CameraImageSource):
        self.__image_source = val

    @property
    def image_file_name(self) -> str:
        return self.__image_file_name

    @image_file_name.setter
    def image_file_name(self, val: str):
        self.__image_file_name = val

    @property
    def web_cam_device_id(self) -> str:
        return self.__web_cam_device_id

    @web_cam_device_id.setter
    def web_cam_device_id(self, val: str):
        self.__web_cam_device_id = val
