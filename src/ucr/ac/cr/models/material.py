class Material:
    def __init__(self, id: int, name: str, unit: str):
        self.id = id
        self.name = name
        self.unit = unit

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "unit": self.unit
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Material":
        return cls(
            id=data["id"],
            name=data["name"],
            unit=data["unit"]
        )

    def __str__(self) -> str:
        return f"Material({self.id}, {self.name}, {self.unit})"