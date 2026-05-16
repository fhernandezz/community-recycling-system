class CollectionPoint:
    def __init__(self, point_id: str, name: str, location: str, district: str,
                 accepted_materials: list, capacity_kg: float,
                 current_load_kg: float = 0.0, is_active: bool = True):
        self.point_id = point_id
        self.name = name
        self.location = location
        self.district = district
        self.accepted_materials = accepted_materials  # list[str]
        self.capacity_kg = float(capacity_kg)
        self.current_load_kg = float(current_load_kg)
        self.is_active = is_active

    def to_dict(self) -> dict:
        return {
            "point_id": self.point_id,
            "name": self.name,
            "location": self.location,
            "district": self.district,
            "accepted_materials": self.accepted_materials,
            "capacity_kg": self.capacity_kg,
            "current_load_kg": self.current_load_kg,
            "is_active": self.is_active
        }

    @classmethod
    def from_dict(cls, data: dict) -> "CollectionPoint":
        return cls(
            point_id=data["point_id"],
            name=data["name"],
            location=data["location"],
            district=data["district"],
            accepted_materials=data["accepted_materials"],
            capacity_kg=data["capacity_kg"],
            current_load_kg=data["current_load_kg"],
            is_active=data["is_active"]
        )