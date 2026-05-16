class RecordController:

    def __init__(self, service):
        self.service = service

    def register_delivery(self, record_id: str, recycler_id: str, point_id: str,
                          material_type: str, weight_kg: float, notes: str = ""):
        return self.service.register_delivery(
            record_id=record_id,
            recycler_id=recycler_id,
            point_id=point_id,
            material_type=material_type,
            weight_kg=weight_kg,
            notes=notes
        )

    def get_top_recyclers(self) -> list:
        return self.service.get_top_recyclers()

    def get_collection_points_status(self) -> list:
        return self.service.get_collection_points_status()

    def get_materials_breakdown(self) -> dict:
        return self.service.get_materials_breakdown()

    def get_records_by_date_range(self, start_date_str: str, end_date_str: str):
        return self.service.get_records_by_date_range(
            start_date_str,
            end_date_str
        )