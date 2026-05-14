from datetime import date as Date

class Delivery:
    def __init__(self, idd: int, user_id: int, material_id: int, point_id: int, quantity: float,
                 delivery_date: str = None):
        self.id = idd
        self.user_id = user_id
        self.material_id = material_id
        self.point_id = point_id
        self.quantity = quantity
        self.delivery_date = delivery_date if delivery_date else Date.today().isoformat()

    def to_dict(self) -> dict:
        return {
            "idd": self.id,
            "user_id": self.user_id,
            "material_id": self.material_id,
            "point_id": self.point_id,
            "quantity": self.quantity,
            "delivery_date": self.delivery_date
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Delivery":
        return cls(
            idd=data["idd"],
            user_id=data["user_id"],
            material_id=data["material_id"],
            point_id=data["point_id"],
            quantity=data["quantity"],
            delivery_date=data["delivery_date"]
        )

    def __str__(self) -> str:
        return f"Delivery({self.id}, user={self.user_id}, material={self.material_id}, quantity={self.quantity})"