from datetime import datetime
from src.ucr.ac.cr.models.recycling_record import RecyclingRecord


class RecordService:
    # Aqui usamos un conjunto SET para consultas rapidas de los materiales validos
    VALID_MATERIALS = {'plástico', 'vidrio', 'papel', 'metal', 'orgánico'}

    def __init__(self, record_repository, recycler_repository, point_repository):
        self._record_repo = record_repository
        self._recycler_repo = recycler_repository
        self._point_repo = point_repository

    # Funciones de validacion
    def _validate_not_empty(self, value: str, field_name: str) -> None:
        if not value or not str(value).strip():
            raise ValueError(f"El campo '{field_name}' no puede estar vacío.")

    def _validate_record_id_unique(self, record_id: str) -> None:
        for record in self._record_repo.get_all():
            if record.record_id == record_id:
                raise ValueError(f"El ID de registro '{record_id}' ya existe.")


    def register_delivery(self, record_id: str, recycler_id: str, point_id: str,
                          material_type: str, weight_kg: float, notes: str = "") -> RecyclingRecord:

        self._validate_not_empty(record_id, "record_id")
        self._validate_not_empty(recycler_id, "recycler_id")
        self._validate_not_empty(point_id, "point_id")
        self._validate_not_empty(material_type, "material_type")
        self._validate_record_id_unique(record_id)

        mat_clean = material_type.strip().lower()

        if mat_clean not in self.VALID_MATERIALS:
            raise ValueError(f"El tipo de material '{material_type}' no es válido en el sistema.")

        if float(weight_kg) <= 0:
            raise ValueError("El peso de la entrega debe ser un número mayor a cero.")

        recycler = self._recycler_repo.get_by_id(recycler_id.strip())
        if not recycler:
            raise ValueError("El reciclador especificado no existe en el sistema.")
        if not recycler.is_active:
            raise ValueError("Operación denegada: El reciclador se encuentra inactivo.")

        point = self._point_repo.get_by_id(point_id.strip())
        if not point:
            raise ValueError("El punto de recolección especificado no existe en el sistema.")
        if not point.is_active:
            raise ValueError("Operación denegada: El punto de recolección está inactivo.")

        if mat_clean not in [material.lower() for material in point.accepted_materials]:
            raise ValueError(f"Este punto de recolección no acepta el material: '{material_type}'.")

        if point.current_load_kg + float(weight_kg) > point.capacity_kg:
            raise ValueError(
                "Transacción abortada: La entrega supera la capacidad máxima restante del punto.")

        point.current_load_kg += float(weight_kg)
        self._point_repo.add(point)

        record = RecyclingRecord(
            record_id=record_id.strip(),
            recycler_id=recycler.recycler_id,
            point_id=point.point_id,
            material_type=mat_clean,
            weight_kg=float(weight_kg),
            record_date=datetime.now().isoformat(),
            notes=notes.strip()
        )
        self._record_repo.add(record)
        return record


    def get_top_recyclers(self) -> list:
        records = self._record_repo.get_all()
        totals = {}

        for record in records:
            if record.recycler_id not in totals:
                totals[record.recycler_id] = [0.0, 0]
            totals[record.recycler_id][0] += record.weight_kg
            totals[record.recycler_id][1] += 1

        tuples_list = []
        for rec_id, metrics in totals.items():
            recycler = self._recycler_repo.get_by_id(rec_id)
            if recycler:
                tuples_list.append((recycler.full_name, recycler.district, metrics[0], metrics[1]))

        return sorted(tuples_list, key=lambda x: x[2], reverse=True)

    def get_collection_points_status(self) -> list:
        points = self._point_repo.get_all()
        status_report = []

        for point in points:
            if point.is_active:
                occupancy = (point.current_load_kg / point.capacity_kg * 100) if point.capacity_kg > 0 else 0.0

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
        breakdown = {material: 0.0 for material in self.VALID_MATERIALS}
        for record in self._record_repo.get_all():
            if record.material_type in breakdown:
                breakdown[record.material_type] += record.weight_kg
        return breakdown

    def get_records_by_date_range(self, start_date_str: str, end_date_str: str) -> dict:
        self._validate_not_empty(start_date_str, "start_date")
        self._validate_not_empty(end_date_str, "end_date")

        filtered_list = []
        total_period_kg = 0.0

        for record in self._record_repo.get_all():
            if start_date_str <= record.record_date <= end_date_str:
                recycler = self._recycler_repo.get_by_id(record.recycler_id)
                point = self._point_repo.get_by_id(record.point_id)

                filtered_list.append({
                    "recycler_name": recycler.full_name if recycler else "Desconocido",
                    "point_name": point.name if point else "Desconocido",
                    "material": record.material_type,
                    "weight": record.weight_kg,
                    "date": record.record_date
                })
                total_period_kg += record.weight_kg

        return {
            "records": filtered_list,
            "total_period_kg": round(total_period_kg, 2)
        }