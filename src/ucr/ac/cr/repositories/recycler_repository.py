import json
from src.ucr.ac.cr.models.recycler import Recycler
from src.ucr.ac.cr.repositories.base_repository import BaseRepository

class RecyclerRepository(BaseRepository[Recycler]):
    def __init__(self, file_path="data/recyclers.json"):
        self.file_path = file_path
        self._storage: list = self._load()

    def _load(self) -> list:
        try:
            with open(self.file_path, "r", encoding="utf-8") as file:
                return [Recycler.from_dict(item) for item in json.load(file)]
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def get_all(self) -> list:
        return self._storage

    def get_by_id(self, recycler_id: str):
        for recycler in self._storage:
            if recycler.recycler_id == recycler_id:
                return recycler
        return None

    def add(self, recycler: Recycler) -> None:
        self._storage.append(recycler)
        self.save_all(self._storage)

    def update(self, recycler: Recycler) -> None:
        """
        Replaces the existing recycler with the same recycler_id in memory
        and persists the change to disk.
        """
        for i, r in enumerate(self._storage):
            if r.recycler_id == recycler.recycler_id:
                self._storage[i] = recycler
                break
        self.save_all(self._storage)

    def save_all(self, recyclers: list) -> None:
        with open(self.file_path, "w", encoding="utf-8") as file:
            json.dump(
                [r.to_dict() for r in recyclers],
                file,
                indent=4,
                ensure_ascii=False
            )