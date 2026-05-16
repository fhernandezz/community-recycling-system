from datetime import datetime
from src.ucr.ac.cr.models.recycling_record import RecyclingRecord

VALID_MATERIALS = {"plástico", "vidrio", "papel", "metal", "orgánico"}


class RecordService:
    """
    Servicio encargado de la gestión de registros de reciclaje.

    Maneja validaciones, creación de registros y generación de reportes
    relacionados con recicladores, puntos de recolección y materiales.
    """

    def __init__(self, repository, recycler_service, point_service):
        """
        Inicializa el servicio con sus dependencias.

        Args:
            repository: Repositorio de registros.
            recycler_service: Servicio de recicladores.
            point_service: Servicio de puntos de recolección.
        """
        self._repository = repository
        self._recycler_service = recycler_service
        self._point_service = point_service

    def _validate_not_empty(self, value: str, field_name: str) -> None:
        """
        Valida que un campo no esté vacío.
        (Regla de validación DRY reutilizable en el sistema)
        """
        if not value or not str(value).strip():
            raise ValueError(f"El campo '{field_name}' no puede estar vacío.")

    def _validate_record_id_unique(self, record_id: str) -> None:
        """
        Valida que el ID del registro no exista previamente.
        """
        for record in self._repository.get_all():
            if record.record_id == record_id:
                raise ValueError(f"El ID de registro '{record_id}' ya existe.")

    def register_delivery(self, record_id: str, recycler_id: str, point_id: str,
                          material_type: str, weight_kg: float, notes: str = "") -> RecyclingRecord:
        """
        Registra una entrega de material reciclable.

        Incluye validaciones de:
        - Campos obligatorios
        - Tipos de material válidos
        - Estado de reciclador y punto
        - Capacidad del punto
        """
        self._validate_not_empty(record_id, "record_id")
        self._validate_not_empty(recycler_id, "recycler_id")
        self._validate_not_empty(point_id, "point_id")
        self._validate_not_empty(material_type, "material_type")
        self._validate_record_id_unique(record_id)

        mat_clean = material_type.strip().lower()

        if mat_clean not in VALID_MATERIALS:
            raise ValueError(f"El tipo de material '{material_type}' no es válido en el sistema.")

        if float(weight_kg) <= 0:
            raise ValueError("El peso de la entrega debe ser un número mayor a cero.")

        recycler = self._recycler_service.get_recycler_by_id(recycler_id.strip())
        if not recycler.is_active:
            raise ValueError("Operación denegada: El reciclador se encuentra inactivo.")

        point = self._point_service.get_point_by_id(point_id.strip())
        if not point.is_active:
            raise ValueError("Operación denegada: El punto de recolección está inactivo.")

        if mat_clean not in [m.lower() for m in point.accepted_materials]:
            raise ValueError(f"Este punto de recolección no acepta el material: '{material_type}'.")

        if point.current_load_kg + float(weight_kg) > point.capacity_kg:
            raise ValueError("Transacción abortada: La entrega supera la capacidad máxima restante del punto.")

        record = RecyclingRecord(
            record_id=record_id.strip(),
            recycler_id=recycler.recycler_id,
            point_id=point.point_id,
            material_type=mat_clean,
            weight_kg=float(weight_kg),
            record_date=datetime.now().isoformat(),
            notes=notes.strip()
        )

        self._repository.add(record)
        self._point_service.add_load(point_id.strip(), float(weight_kg))

        return record

    def get_all_records(self) -> list:
        """Retorna todos los registros almacenados."""
        return self._repository.get_all()

    def get_records_by_recycler(self, recycler_id: str) -> list:
        """Filtra registros por reciclador."""
        self._recycler_service.get_recycler_by_id(recycler_id)
        return [r for r in self._repository.get_all() if r.recycler_id == recycler_id]

    def get_records_by_point(self, point_id: str) -> list:
        """Filtra registros por punto de recolección."""
        self._point_service.get_point_by_id(point_id)
        return [r for r in self._repository.get_all() if r.point_id == point_id]

    def get_top_recyclers(self) -> list:
        """
        Reporte: Top recicladores por kg total.

        - Usa diccionario acumulador
        - Convierte a lista de tuplas
        - Ordena con sorted() y lambda por kg total
        """
        totals = {}
        for record in self._repository.get_all():
            if record.recycler_id not in totals:
                totals[record.recycler_id] = [0.0, 0]
            totals[record.recycler_id][0] += record.weight_kg
            totals[record.recycler_id][1] += 1

        tuples_list = []
        for rec_id, metrics in totals.items():
            try:
                recycler = self._recycler_service.get_recycler_by_id(rec_id)
                tuples_list.append((recycler.full_name, recycler.district, metrics[0], metrics[1]))
            except ValueError:
                continue

        return sorted(tuples_list, key=lambda x: x[2], reverse=True)

    def get_collection_points_status(self) -> list:
        """Reporte de estado de puntos de recolección con nivel de ocupación."""
        status_report = []
        for point in self._point_service.list_active_points():
            occupancy = self._point_service.calculate_occupancy_percentage(point)

            if occupancy > 80.0:
                alert = "Crítico"
            elif occupancy > 60.0:
                alert = "Atención"
            else:
                alert = "Normal"

            status_report.append({
                "name": point.name,
                "current_load": point.current_load_kg,
                "max_capacity": point.capacity_kg,
                "percentage": round(occupancy, 2),
                "status": alert
            })

        return status_report

    def get_materials_breakdown(self) -> dict:
        """
        Reporte: total de kg por tipo de material.

        (Uso de diccionario acumulador agrupado por categoría)
        """
        breakdown = {material: 0.0 for material in VALID_MATERIALS}

        for record in self._repository.get_all():
            if record.material_type in breakdown:
                breakdown[record.material_type] += record.weight_kg

        return breakdown

    def get_records_by_date_range(self, start_date_str: str, end_date_str: str) -> dict:
        """
        Filtra registros por rango de fechas ISO 8601.

        Retorna:
            - lista de registros enriquecidos
            - total de kg en el periodo
        """
        self._validate_not_empty(start_date_str, "start_date")
        self._validate_not_empty(end_date_str, "end_date")

        if start_date_str > end_date_str:
            raise ValueError("La fecha de inicio no puede ser posterior a la fecha de fin.")

        filtered_list = []
        total_period_kg = 0.0

        for record in self._repository.get_all():
            if start_date_str <= record.record_date <= end_date_str:

                try:
                    recycler = self._recycler_service.get_recycler_by_id(record.recycler_id)
                    recycler_name = recycler.full_name
                except ValueError:
                    recycler_name = "Desconocido"

                try:
                    point = self._point_service.get_point_by_id(record.point_id)
                    point_name = point.name
                except ValueError:
                    point_name = "Desconocido"

                filtered_list.append({
                    "recycler_name": recycler_name,
                    "point_name": point_name,
                    "material": record.material_type,
                    "weight": record.weight_kg,
                    "date": record.record_date
                })

                total_period_kg += record.weight_kg

        return {
            "records": filtered_list,
            "total_period_kg": round(total_period_kg, 2)
        }