from src.ucr.ac.cr.models.collection_point import CollectionPoint


class CollectionPointService:
    """
    Servicio encargado de la gestión de puntos de recolección.

    Responsabilidades:
    - Registro de puntos
    - Validaciones de negocio
    - Consulta de puntos
    - Gestión de estado (activo/inactivo)
    - Control de capacidad y carga

    Actúa como capa intermedia entre el repositorio y la lógica del sistema.
    """

    def __init__(self, repository):
        """
        Inicializa el servicio con su repositorio.

        Args:
            repository: Repositorio de puntos de recolección.
        """
        self._repository = repository

    def _validate_not_empty(self, value: str, field_name: str) -> None:
        """
        Valida que un campo obligatorio no esté vacío.
        """
        if not value or not str(value).strip():
            raise ValueError(f"El campo '{field_name}' no puede estar vacío.")

    def _validate_capacity(self, capacity_kg: float) -> None:
        """
        Valida que la capacidad del punto sea mayor a 0.
        """
        if float(capacity_kg) <= 0:
            raise ValueError("La capacidad máxima debe ser un número positivo mayor a 0.")

    def _validate_point_id_unique(self, point_id: str) -> None:
        """
        Verifica que el ID del punto no exista previamente.
        """
        for point in self._repository.get_all():
            if point.point_id == point_id:
                raise ValueError(
                    f"El ID del punto de recolección '{point_id}' ya existe."
                )

    def register_collection_point(self, point_id: str, name: str, location: str,
                                  district: str, accepted_materials: list,
                                  capacity_kg: float) -> CollectionPoint:
        """
        Registra un nuevo punto de recolección en el sistema.

        Valida:
        - Campos obligatorios
        - Capacidad válida
        - Materiales aceptados
        - Unicidad del ID

        Retorna:
            CollectionPoint: punto creado y almacenado.
        """
        self._validate_not_empty(point_id, "point_id")
        self._validate_not_empty(name, "name")
        self._validate_not_empty(location, "location")
        self._validate_not_empty(district, "district")

        if not accepted_materials:
            raise ValueError("Debe seleccionar al menos un material aceptado para este punto.")

        self._validate_capacity(capacity_kg)
        self._validate_point_id_unique(point_id)

        cleaned_materials = [
            m.strip().lower()
            for m in accepted_materials
            if m.strip()
        ]

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
        """Retorna todos los puntos de recolección registrados."""
        return self._repository.get_all()

    def get_point_by_id(self, point_id: str) -> CollectionPoint:
        """
        Obtiene un punto de recolección por su ID.

        Lanza error si no existe.
        """
        self._validate_not_empty(point_id, "point_id")

        point = self._repository.get_by_id(point_id)

        if not point:
            raise ValueError(
                f"Punto de recolección con ID '{point_id}' no encontrado."
            )

        return point

    def list_active_points(self) -> list:
        """Retorna solo los puntos de recolección activos."""
        return [
            p
            for p in self._repository.get_all()
            if p.is_active
        ]

    def calculate_occupancy_percentage(self, point: CollectionPoint) -> float:
        """
        Calcula el porcentaje de ocupación de un punto.

        Returns:
            float: porcentaje de ocupación (0-100)
        """
        if point.capacity_kg == 0:
            return 0.0

        return (point.current_load_kg / point.capacity_kg) * 100

    def add_load(self, point_id: str, weight_kg: float) -> CollectionPoint:
        """
        Aumenta la carga actual de un punto de recolección.

        Usado después de registrar una entrega exitosa.
        """
        point = self.get_point_by_id(point_id)
        point.current_load_kg += float(weight_kg)
        self._repository.update(point)
        return point

    def set_active_status(self, point_id: str, is_active: bool) -> CollectionPoint:
        """
        Activa o desactiva un punto de recolección.
        """
        point = self.get_point_by_id(point_id)
        point.is_active = is_active
        self._repository.update(point)
        return point