class User:
    def __init__(self, id: int, name: str, id_number: str, phone: str, email: str):
        self.id = id
        self.name = name
        self.id_number = id_number
        self.phone = phone
        self.email = email

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "id_number": self.id_number,
            "phone": self.phone,
            "email": self.email
        }

    @classmethod
    def from_dict(cls, data: dict) -> "User":
        return cls(
            id=data["id"],
            name=data["name"],
            id_number=data["id_number"],
            phone=data["phone"],
            email=data["email"]
        )

    def __str__(self) -> str:
        return f"User({self.id}, {self.name}, {self.id_number})"