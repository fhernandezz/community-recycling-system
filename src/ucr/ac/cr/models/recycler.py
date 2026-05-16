class Recycler:
    def __init__(self, recycler_id: str, full_name: str, id_number: str,
                 email: str, phone: str, district: str,
                 registration_date: str, is_active: bool = True):
        self.recycler_id = recycler_id
        self.full_name = full_name
        self.id_number = id_number
        self.email = email
        self.phone = phone
        self.district = district
        self.registration_date = registration_date
        self.is_active = is_active

    def to_dict(self) -> dict:
        return {
            "recycler_id": self.recycler_id,
            "full_name": self.full_name,
            "id_number": self.id_number,
            "email": self.email,
            "phone": self.phone,
            "district": self.district,
            "registration_date": self.registration_date,
            "is_active": self.is_active
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Recycler":
        return cls(
            recycler_id=data["recycler_id"],
            full_name=data["full_name"],
            id_number=data["id_number"],
            email=data["email"],
            phone=data["phone"],
            district=data["district"],
            registration_date=data["registration_date"],
            is_active=data["is_active"]
        )