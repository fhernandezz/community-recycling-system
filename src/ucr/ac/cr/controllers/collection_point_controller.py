class CollectionPointController:

    def __init__(self, service):
        self.service = service

    def register_collection_point(self, point_id: str, name: str, location: str,
                                  district: str, accepted_materials: list, capacity_kg: float):
        return self.service.register_collection_point(
            point_id=point_id,
            name=name,
            location=location,
            district=district,
            accepted_materials=accepted_materials,
            capacity_kg=capacity_kg
        )

    def get_all_points(self) -> list:
        return self.service.get_all_points()

    def get_point_by_id(self, point_id: str):
        return self.service.get_point_by_id(point_id)

    def list_active_points(self) -> list:
        return self.service.list_active_points()

    def set_active_status(self, point_id: str, is_active: bool):
        return self.service.set_active_status(point_id, is_active)