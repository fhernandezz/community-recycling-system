import json
from src.ucr.ac.cr.models.recycling_record import RecyclingRecord
from src.ucr.ac.cr.repositories.base_repository import BaseRepository

class RecordRepository(BaseRepository[RecyclingRecord]):

    def __init__(self, file_path="data/records.json"):
        self.file_path = file_path
        self._storage: list = self._load()

    def _load(self) -> list:
        try:
            with open(self.file_path, "r", encoding="utf-8") as file:
                return [RecyclingRecord.from_dict(item) for item in json.load(file)]
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def get_all(self) -> list:
        return self._storage

    def get_by_id(self, record_id: str):
        for record in self._storage:
            if record.record_id == record_id:
                return record
        return None

    def add(self, record: RecyclingRecord) -> None:
        self._storage.append(record)
        self.save_all(self._storage)

    def update(self, record: RecyclingRecord) -> None:
        for i, r in enumerate(self._storage):
            if r.record_id == record.record_id:
                self._storage[i] = record
                break
        self.save_all(self._storage)

    def save_all(self, records: list) -> None:
        with open(self.file_path, "w", encoding="utf-8") as file:
            json.dump(
                [r.to_dict() for r in records],
                file,
                indent=4,
                ensure_ascii=False
            )