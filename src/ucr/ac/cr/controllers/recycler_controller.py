class RecyclerController:

    def __init__(self, service):
        self.service = service

    def register_recycler(self, recycler_id: str, full_name: str, id_number: str,
                          email: str, phone: str, district: str):
        return self.service.register_recycler(
            recycler_id=recycler_id,
            full_name=full_name,
            id_number=id_number,
            email=email,
            phone=phone,
            district=district
        )

    def get_all_recyclers(self) -> list:
        return self.service.get_all_recyclers()

    def get_recycler_by_id(self, recycler_id: str):
        return self.service.get_recycler_by_id(recycler_id)

    def get_recyclers_by_district(self, district: str) -> list:
        return self.service.get_recyclers_by_district(district)

    def set_active_status(self, recycler_id: str, is_active: bool):
        return self.service.set_active_status(recycler_id, is_active)

    def validate_credentials(self, recycler_id: str, password: str) -> bool:
        return self.service.validate_credentials(recycler_id, password)