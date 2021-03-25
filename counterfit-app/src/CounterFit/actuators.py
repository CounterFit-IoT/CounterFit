from abc import ABC, abstractmethod
from enum import Enum

class ActuatorType(Enum):
    FLOAT = 1
    BOOLEAN = 2

class ActuatorBase(ABC):
    def __init__(self, pin:int):
        self.__pin = pin
    
    @staticmethod
    @abstractmethod
    def actuator_name() -> str:
        pass

    @staticmethod
    @abstractmethod
    def actuator_type() -> ActuatorType:
        pass

    @property
    def pin(self) -> int:
        return self.__pin

class FloatActuatorBase(ActuatorBase):
    def __init__(self, pin:int):

        super().__init__(pin)
        self.__value = 0

    @staticmethod
    @abstractmethod
    def actuator_name() -> str:
        pass

    @staticmethod
    def actuator_type() -> ActuatorType:
        return ActuatorType.FLOAT

    @property
    def value(self) -> float:
        return self.__value

    @value.setter
    def value(self, val: float):
        self.__value = val

class BooleanActuatorBase(ActuatorBase):
    def __init__(self, pin:int):

        super().__init__(pin)

        self.__value = False

    @staticmethod
    @abstractmethod
    def actuator_name() -> str:
        pass

    @staticmethod
    def actuator_type() -> ActuatorType:
        return ActuatorType.BOOLEAN

    @property
    def value(self) -> bool:
        return self.__value

    @value.setter
    def value(self, val: bool):
        self.__value = val

class LedActuator(BooleanActuatorBase):
    def __init__(self, pin):
        super().__init__(pin)
        self.__color = "#FF0000"

    @staticmethod
    def actuator_name() -> str:
        return 'LED'
    
    @property
    def color(self) -> str:
        return self.__color

    @color.setter
    def color(self, val: str):
        self.__color = val
