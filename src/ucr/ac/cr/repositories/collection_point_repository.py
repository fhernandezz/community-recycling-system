import json
from src.ucr.ac.cr.models.collection_point import CollectionPoint
from src.ucr.ac.cr.repositories.base_repository import BaseRepository

class CollectionPointRepository(BaseRepository[CollectionPoint]):
    def __init__(self, file_path="data/collection_points.json"):
        self.file_path = file_path
        self._storage: list = self._load()

    def _load(self) -> list:
        try:
            with open(self.file_path, "r", encoding="utf-8") as file:
                return [CollectionPoint.from_dict(item) for item in json.load(file)]
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def get_all(self) -> list:
        return self._storage

    def get_by_id(self, point_id: str):
        for point in self._storage:
            if point.point_id == point_id:
                return point
        return None

    def add(self, point: CollectionPoint) -> None:
        self._storage.append(point)
        self.save_all(self._storage)

    def update(self, point: CollectionPoint) -> None:
        for i, p in enumerate(self._storage):
            if p.point_id == point.point_id:
                self._storage[i] = point
                break
        self.save_all(self._storage)

    def save_all(self, points: list) -> None:
        with open(self.file_path, "w", encoding="utf-8") as file:
            json.dump(
                [p.to_dict() for p in points],
                file,
                indent=4,
                ensure_ascii=False
            )