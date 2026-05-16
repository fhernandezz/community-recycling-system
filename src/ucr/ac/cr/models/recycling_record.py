class RecyclingRecord:
    def __init__(self, record_id: str, recycler_id: str, point_id: str,
                 material_type: str, weight_kg: float, record_date: str, notes: str = ""):
        self.record_id = record_id
        self.recycler_id = recycler_id
        self.point_id = point_id
        self.material_type = material_type
        self.weight_kg = float(weight_kg)
        self.record_date = record_date
        self.notes = notes

    def to_dict(self) -> dict:
        return {
            "record_id": self.record_id,
            "recycler_id": self.recycler_id,
            "point_id": self.point_id,
            "material_type": self.material_type,
            "weight_kg": self.weight_kg,
            "record_date": self.record_date,
            "notes": self.notes
        }

    @classmethod
    def from_dict(cls, data: dict) -> "RecyclingRecord":
        return cls(
            record_id=data["record_id"],
            recycler_id=data["recycler_id"],
            point_id=data["point_id"],
            material_type=data["material_type"],
            weight_kg=data["weight_kg"],
            record_date=data["record_date"],
            notes=data.get("notes", "")
        )