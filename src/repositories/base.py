from abc import ABC, abstractmethod
from typing import TypeVar, Generic, Optional, List


T = TypeVar("T")

class BaseRepository(Generic[T], ABC):
    def __init__(self, connection) -> None:
        self.connection = connection

    @abstractmethod
    def save(self, entity: T) -> T:
        pass

    @abstractmethod
    def find_by_id(self, id_value: str) -> Optional[T]:
        pass

    @abstractmethod
    def find_all(self) -> List[T]:
        pass

    @abstractmethod
    def delete(self, id_value: str) -> bool:
        pass