from abc import ABC, abstractmethod
from typing import TypeVar, Generic

T = TypeVar("T")


class BaseRepository(ABC, Generic[T]):
    @abstractmethod
    def get_all(self) -> list:
        pass

    @abstractmethod
    def get_by_id(self, entity_id):
        pass

    @abstractmethod
    def add(self, entity: T) -> None:
        pass

    @abstractmethod
    def update(self, entity: T) -> None:
        pass

    @abstractmethod
    def save_all(self, entities: list) -> None:
        pass