from abc import abstractmethod
from enum import Enum
from typing import List
import random

from CounterFit.sensors import SensorBase, SensorType


class I2CSensorBase(SensorBase):
    @staticmethod
    def sensor_type() -> SensorType:
        return SensorType.I2C

    @staticmethod
    @abstractmethod
    def sensor_unit_type() -> SensorType:
        pass

    @staticmethod
    @abstractmethod
    def sensor_name() -> str:
        pass

    @property
    def id(self) -> str:
        return self.port

    @property
    def address(self) -> str:
        return f"0x{int(self.port):02x}"


class FloatI2CSensorBase(I2CSensorBase):
    def __init__(self, port: str, valid_min: float, valid_max: float):
        super().__init__(port)

        self.__valid_min = valid_min
        self.__valid_max = valid_max
        self.value = valid_min
        self.random_min = float(valid_min)
        self.random_max = float(valid_max)

    @staticmethod
    @abstractmethod
    def sensor_name() -> str:
        pass

    @staticmethod
    @abstractmethod
    def sensor_units() -> List[str]:
        pass

    @staticmethod
    def sensor_unit_type() -> SensorType:
        return SensorType.FLOAT

    @property
    @abstractmethod
    def unit(self) -> str:
        pass

    @property
    def value(self) -> float:
        if self._random:
            return round(random.uniform(self.__random_min, self.__random_max), 2)

        return self.__value

    @value.setter
    def value(self, val: float):
        if val < self.__valid_min or val > self.__valid_max:
            raise ValueError()
        self.__value = val

    @property
    def random_min(self) -> float:
        return self.__random_min

    @random_min.setter
    def random_min(self, val: float):
        if val < self.__valid_min or val > self.__valid_max:
            raise ValueError()
        self.__random_min = val

    @property
    def random_max(self) -> float:
        return self.__random_max

    @random_max.setter
    def random_max(self, val: float):
        if val < self.__valid_min or val > self.__valid_max:
            raise ValueError()
        self.__random_max = val

    @property
    def valid_min(self) -> float:
        return self.__valid_min

    @property
    def valid_max(self) -> float:
        return self.__valid_max


class IntegerI2CSensorBase(I2CSensorBase):
    def __init__(self, port: str, valid_min: int, valid_max: int):
        super().__init__(port)

        self.__valid_min = valid_min
        self.__valid_max = valid_max
        self.value = valid_min
        self.random_min = int(valid_min)
        self.random_max = int(valid_max)

    @staticmethod
    @abstractmethod
    def sensor_name() -> str:
        pass

    @staticmethod
    @abstractmethod
    def sensor_units() -> List[str]:
        pass

    @staticmethod
    def sensor_unit_type() -> SensorType:
        return SensorType.INTEGER

    @property
    @abstractmethod
    def unit(self) -> str:
        pass

    @property
    def value(self) -> int:
        if self._random:
            return random.randint(self.__random_min, self.__random_max)

        return self.__value

    @value.setter
    def value(self, val: int):
        if val < self.__valid_min or val > self.__valid_max:
            raise ValueError()
        self.__value = val

    @property
    def random_min(self) -> int:
        return self.__random_min

    @random_min.setter
    def random_min(self, val: int):
        if val < self.__valid_min or val > self.__valid_max:
            raise ValueError()
        self.__random_min = val

    @property
    def random_max(self) -> int:
        return self.__random_max

    @random_max.setter
    def random_max(self, val: int):
        if val < self.__valid_min or val > self.__valid_max:
            raise ValueError()
        self.__random_max = val

    @property
    def valid_min(self) -> int:
        return self.__valid_min

    @property
    def valid_max(self) -> int:
        return self.__valid_max


# pylint: disable=C0103
class DistanceUnit(Enum):
    Millimeter = 1


class DistanceSensor(IntegerI2CSensorBase):
    def __init__(self, port: str, unit):
        if isinstance(unit, str):
            unit = DistanceUnit[unit]

        self.__unit = unit

        super().__init__(port, 0, 999999)

    @staticmethod
    def sensor_name() -> str:
        return "Distance"

    @property
    def unit(self) -> str:
        return self.__unit.name

    @staticmethod
    def sensor_units() -> List[str]:
        return [DistanceUnit.Millimeter.name]
