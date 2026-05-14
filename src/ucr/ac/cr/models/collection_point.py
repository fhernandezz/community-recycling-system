class CollectionPoint:
    def __init__(self, id: int, name: str, address: str):
        self.id = id
        self.name = name
        self.address = address

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "address": self.address
        }

    @classmethod
    def from_dict(cls, data: dict) -> "CollectionPoint":
        return cls(
            id=data["id"],
            name=data["name"],
            address=data["address"]
        )

    def __str__(self) -> str:
        return f"CollectionPoint({self.id}, {self.name})"