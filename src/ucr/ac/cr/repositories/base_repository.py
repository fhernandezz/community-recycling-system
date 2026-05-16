from abc import ABC, abstractmethod
from typing import TypeVar, Generic

T = TypeVar("T")


class BaseRepository(ABC, Generic[T]):
    """
    Generic base repository that defines the contract all concrete
    repositories must fulfill (OCP + LSP).

    Using ABC enforces the contract at instantiation time: if a subclass
    doesn't implement every abstract method, Python raises TypeError
    before the program even starts running.
    """

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