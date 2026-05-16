from abc import ABC, abstractmethod
from typing import TypeVar, Generic

T = TypeVar("T")

class BaseRepository(ABC, Generic[T]):

    @abstractmethod
    def get_all(self) -> list:
        ...

    @abstractmethod
    def get_by_id(self, entity_id):
        ...

    @abstractmethod
    def add(self, entity: T) -> None:
        ...

    @abstractmethod
    def update(self, entity: T) -> None:
        ...

    @abstractmethod
    def save_all(self, entities: list) -> None:
        ...