import json
from src.ucr.ac.cr.models.collection_point import CollectionPoint

class CollectionPointRepository:

    def __init__(self, file_path="data/collection_points.json"):
        self.file_path = file_path

    def get_all(self):
        try:
            with open(self.file_path, "r", encoding="utf-8") as file:
                data = json.load(file)
            return [CollectionPoint.from_dict(item) for item in data]
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def get_by_id(self, point_id: str):
        for point in self.get_all():
            if point.point_id == point_id:
                return point
        return None

    def add(self, point: CollectionPoint):
        points = self.get_all()
        points.append(point)
        self.save_all(points)

    def save_all(self, points):
        with open(self.file_path, "w", encoding="utf-8") as file:
            json.dump(
                [point.to_dict() for point in points],
                file,
                indent=4,
                ensure_ascii=False
            )