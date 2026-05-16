import json
from src.ucr.ac.cr.models.recycler import Recycler


class RecyclerRepository:

    def __init__(self, file_path="data/recyclers.json"):
        self.file_path = file_path

    def get_all(self):
        try:
            with open(self.file_path, "r", encoding="utf-8") as file:
                data = json.load(file)
            return [Recycler.from_dict(item) for item in data]
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def get_by_id(self, recycler_id: str):
        for recycler in self.get_all():
            if recycler.recycler_id == recycler_id:
                return recycler
        return None

    def add(self, recycler: Recycler):
        recyclers = self.get_all()
        recyclers.append(recycler)
        self.save_all(recyclers)

    def save_all(self, recyclers):
        with open(self.file_path, "w", encoding="utf-8") as file:
            json.dump(
                [recycler.to_dict() for recycler in recyclers],
                file,
                indent=4,
                ensure_ascii=False
            )