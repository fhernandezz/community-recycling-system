import json
from models.collection_point import CollectionPoint


class CollectionPointRepository:

    def __init__(self, file_path="data/collection_points.json"):
        self.file_path = file_path

    def get_all(self):
        with open(self.file_path, "r") as file:
            data = json.load(file)

        return [CollectionPoint.from_dict(item) for item in data]

    def add(self, point: CollectionPoint):
        points = self.get_all()

        points.append(point)

        self.save_all(points)

    def save_all(self, points):
        with open(self.file_path, "w") as file:
            json.dump(
                [p.to_dict() for p in points],
                file,
                indent=4
            )