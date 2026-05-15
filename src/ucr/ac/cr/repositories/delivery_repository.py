import json
from models.delivery import Delivery


class DeliveryRepository:

    def __init__(self, file_path="data/deliveries.json"):
        self.file_path = file_path

    def get_all(self):
        with open(self.file_path, "r") as file:
            data = json.load(file)

        return [Delivery.from_dict(item) for item in data]

    def add(self, delivery: Delivery):
        deliveries = self.get_all()

        deliveries.append(delivery)

        self.save_all(deliveries)

    def save_all(self, deliveries):
        with open(self.file_path, "w") as file:
            json.dump(
                [d.to_dict() for d in deliveries],
                file,
                indent=4
            )