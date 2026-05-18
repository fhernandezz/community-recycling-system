from datetime import datetime
from src.ucr.ac.cr.models.recycling_record import RecyclingRecord

VALID_MATERIALS = {"plástico", "vidrio", "papel", "metal", "orgánico"}


class RecordService:

    def __init__(self, repository, recycler_service, point_service):
        self._repository = repository
        self._recycler_service = recycler_service
        self._point_service = point_service

    def _validate_not_empty(self, value: str, field_name: str) -> None:
        if not value or not str(value).strip():
            raise ValueError(f"El campo {field_name} no puede estar vacío.")

    def _validate_record_id_unique(self, record_id: str) -> None:
        for existing_record in self._repository.get_all():
            if existing_record.record_id == record_id:
                raise ValueError(f"El ID de registro {record_id} ya existe.")

    def register_delivery(self, record_id: str, recycler_id: str, point_id: str,
                          material_type: str, weight_kg: float, notes: str = "") -> RecyclingRecord:
        self._validate_not_empty(record_id, "record_id")
        self._validate_not_empty(recycler_id, "recycler_id")
        self._validate_not_empty(point_id, "point_id")
        self._validate_not_empty(material_type, "material_type")
        self._validate_record_id_unique(record_id)

        clean_material = material_type.strip().lower()

        if clean_material not in VALID_MATERIALS:
            raise ValueError(f"El tipo de material '{material_type}' no es válido en el sistema.")

        if float(weight_kg) <= 0:
            raise ValueError("El peso de la entrega debe ser un número mayor a cero.")

        found_recycler = self._recycler_service.get_recycler_by_id(recycler_id.strip())
        if not found_recycler.is_active:
            raise ValueError("Operación denegada: El reciclador se encuentra inactivo.")

        found_point = self._point_service.get_point_by_id(point_id.strip())
        if not found_point.is_active:
            raise ValueError("Operación denegada: El punto de recolección está inactivo.")

        if clean_material not in [accepted.lower() for accepted in found_point.accepted_materials]:
            raise ValueError(f"Este punto de recolección no acepta el material: '{material_type}'.")

        if found_point.current_load_kg + float(weight_kg) > found_point.capacity_kg:
            raise ValueError("Transacción abortada: La entrega supera la capacidad máxima restante del punto.")

        new_record = RecyclingRecord(
            record_id=record_id.strip(),
            recycler_id=found_recycler.recycler_id,
            point_id=found_point.point_id,
            material_type=clean_material,
            weight_kg=float(weight_kg),
            record_date=datetime.now().isoformat(),
            notes=notes.strip()
        )

        self._repository.add(new_record)
        self._point_service.add_load(point_id.strip(), float(weight_kg))

        return new_record

    def get_all_records(self) -> list:
        return self._repository.get_all()

    def get_records_by_recycler(self, recycler_id: str) -> list:
        self._recycler_service.get_recycler_by_id(recycler_id)
        return [
            existing_record
            for existing_record in self._repository.get_all()
            if existing_record.recycler_id == recycler_id
        ]

    def get_records_by_point(self, point_id: str) -> list:
        self._point_service.get_point_by_id(point_id)
        return [
            existing_record
            for existing_record in self._repository.get_all()
            if existing_record.point_id == point_id
        ]

    def get_top_recyclers(self) -> list:
        # acumula el total de kg y visitas por reciclador
        totals_per_recycler = {}

        for delivery_record in self._repository.get_all():
            if delivery_record.recycler_id not in totals_per_recycler:
                totals_per_recycler[delivery_record.recycler_id] = [0.0, 0]
            totals_per_recycler[delivery_record.recycler_id][0] += delivery_record.weight_kg
            totals_per_recycler[delivery_record.recycler_id][1] += 1

        # arma la lista de tuplas con los datos de cada reciclador
        recycler_tuples = []
        for recycler_id, metrics in totals_per_recycler.items():
            try:
                found_recycler = self._recycler_service.get_recycler_by_id(recycler_id)
                recycler_tuples.append(
                    (found_recycler.full_name, found_recycler.district, metrics[0], metrics[1])
                )
            except ValueError:
                continue

        # ordena de mayor a menor por kg total
        return sorted(recycler_tuples, key=lambda x: x[2], reverse=True)

    def get_collection_points_status(self) -> list:
        status_report = []

        for active_point in self._point_service.list_active_points():
            occupancy_percentage = self._point_service.calculate_occupancy_percentage(active_point)

            if occupancy_percentage > 80.0:
                alert_label = "Crítico"
            elif occupancy_percentage > 60.0:
                alert_label = "Atención"
            else:
                alert_label = "Normal"

            status_report.append({
                "name": active_point.name,
                "current_load": active_point.current_load_kg,
                "max_capacity": active_point.capacity_kg,
                "percentage": round(occupancy_percentage, 2),
                "status": alert_label
            })

        return status_report

    def get_materials_breakdown(self) -> dict:
        # inicializa todos los materiales en 0 y va sumando
        kg_per_material = {material_name: 0.0 for material_name in VALID_MATERIALS}

        for delivery_record in self._repository.get_all():
            if delivery_record.material_type in kg_per_material:
                kg_per_material[delivery_record.material_type] += delivery_record.weight_kg

        return kg_per_material

    def get_records_by_date_range(self, start_date_str: str, end_date_str: str) -> dict:
        self._validate_not_empty(start_date_str, "start_date")
        self._validate_not_empty(end_date_str, "end_date")

        # si solo viene la fecha sin hora, se completa automáticamente
        start_normalized = start_date_str if "T" in start_date_str else start_date_str + "T00:00:00"
        end_normalized = end_date_str if "T" in end_date_str else end_date_str + "T23:59:59"

        if start_normalized > end_normalized:
            raise ValueError("La fecha de inicio no puede ser posterior a la fecha de fin.")

        filtered_records = []
        total_period_kg = 0.0

        for delivery_record in self._repository.get_all():
            if start_normalized <= delivery_record.record_date <= end_normalized:

                try:
                    found_recycler = self._recycler_service.get_recycler_by_id(delivery_record.recycler_id)
                    recycler_name = found_recycler.full_name
                except ValueError:
                    recycler_name = "Desconocido"

                try:
                    found_point = self._point_service.get_point_by_id(delivery_record.point_id)
                    point_name = found_point.name
                except ValueError:
                    point_name = "Desconocido"

                filtered_records.append({
                    "recycler_name": recycler_name,
                    "point_name": point_name,
                    "material": delivery_record.material_type,
                    "weight": delivery_record.weight_kg,
                    "date": delivery_record.record_date
                })

                total_period_kg += delivery_record.weight_kg

        return {
            "records": filtered_records,
            "total_period_kg": round(total_period_kg, 2)
        }