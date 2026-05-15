import json
from models.material import Material


class MaterialRepository:

    def __init__(self, file_path="data/materials.json"):
        self.file_path = file_path

    def get_all(self):
        with open(self.file_path, "r") as file:
            data = json.load(file)

        return [Material.from_dict(item) for item in data]

    def add(self, material: Material):
        materials = self.get_all()

        materials.append(material)

        self.save_all(materials)

    def save_all(self, materials):
        with open(self.file_path, "w") as file:
            json.dump(
                [m.to_dict() for m in materials],
                file,
                indent=4
            )