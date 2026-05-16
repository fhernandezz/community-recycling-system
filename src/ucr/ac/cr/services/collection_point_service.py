from src.ucr.ac.cr.models.collection_point import CollectionPoint


class CollectionPointService:

    def __init__(self, repository):
        self._repository = repository

    # Metodos de validacion para no repetir codigo
    def _validate_not_empty(self, value: str, field_name: str) -> None:
        if not value or not str(value).strip():
            raise ValueError(f"El campo '{field_name}' no puede estar vacío.")

    def _validate_capacity(self, capacity_kg: float) -> None:
        if float(capacity_kg) <= 0:
            raise ValueError("La capacidad máxima debe ser un número positivo mayor a 0.")

    def _validate_point_id_unique(self, point_id: str) -> None:
        for point in self._repository.get_all():
            if point.point_id == point_id:
                raise ValueError(f"El ID del punto de recolección '{point_id}' ya existe.")

    # De aca para abajo estan los metodos de el servicio con su  logica de negocio
    def register_collection_point(self, point_id: str, name: str, location: str,
                                  district: str, accepted_materials: list,
                                  capacity_kg: float) -> CollectionPoint:
        self._validate_not_empty(point_id, "point_id")
        self._validate_not_empty(name, "name")
        self._validate_not_empty(location, "location")
        self._validate_not_empty(district, "district")

        if not accepted_materials:
            raise ValueError("Debe seleccionar al menos un material aceptado para este punto.")

        self._validate_capacity(capacity_kg)
        self._validate_point_id_unique(point_id)

        cleaned_materials = [material.strip().lower() for material in accepted_materials if
                             material.strip()]

        point = CollectionPoint(
            point_id=point_id.strip(),
            name=name.strip(),
            location=location.strip(),
            district=district.strip(),
            accepted_materials=cleaned_materials,
            capacity_kg=float(capacity_kg),
            current_load_kg=0.0,
            is_active=True
        )
        self._repository.add(point)
        return point

    def get_all_points(self) -> list:
        return self._repository.get_all()

    def get_point_by_id(self, point_id: str) -> CollectionPoint:
        self._validate_not_empty(point_id, "point_id")
        point = self._repository.get_by_id(point_id)
        if not point:
            raise ValueError(f"Punto de recolección con ID '{point_id}' no encontrado.")
        return point

    def list_active_points(self) -> list:
        return [point for point in self._repository.get_all() if point.is_active]

    def calculate_occupancy_percentage(self, point: CollectionPoint) -> float:
        if point.capacity_kg == 0:
            return 0.0
        return (point.current_load_kg / point.capacity_kg) * 100

    def set_active_status(self, point_id: str, is_active: bool) -> CollectionPoint:
        point = self.get_point_by_id(point_id)
        point.is_active = is_active
        self._repository.add(point)
        return point