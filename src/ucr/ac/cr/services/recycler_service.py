from datetime import datetime
from src.ucr.ac.cr.models.recycler import Recycler

class RecyclerService:
    def __init__(self, repository):
        self._repository = repository

    # Aca estan las funciones de validacion para evitar repetir  codigo
    def _validate_not_empty(self, value: str, field_name: str) -> None:
        if not value or not str(value).strip():
            raise ValueError(f"El campo '{field_name}' no puede estar vacío.")

    def _validate_email_format(self, email: str) -> None:
        if "@" not in email:
            raise ValueError(f"El correo '{email}' no tiene un formato válido.")

    def _validate_id_number_unique(self, id_number: str) -> None:
        for recycler in self._repository.get_all():
            if recycler.id_number == id_number:
                raise ValueError(f"Ya existe un reciclador registrado con la cédula '{id_number}'.")

    def _validate_recycler_id_unique(self, recycler_id: str) -> None:
        for recycler in self._repository.get_all():
            if recycler.recycler_id == recycler_id:
                raise ValueError(f"El ID de reciclador '{recycler_id}' ya existe.")

    # De aqui para abajo estan los metodos de el servicio como tal con logica de negocio

    def register_recycler(self, recycler_id: str, full_name: str, id_number: str,
                          email: str, phone: str, district: str) -> Recycler:
        self._validate_not_empty(recycler_id, "recycler_id")
        self._validate_not_empty(full_name, "full_name")
        self._validate_not_empty(id_number, "id_number")
        self._validate_not_empty(email, "email")
        self._validate_not_empty(phone, "phone")
        self._validate_not_empty(district, "district")

        self._validate_email_format(email)
        self._validate_recycler_id_unique(recycler_id)
        self._validate_id_number_unique(id_number)

        recycler = Recycler(
            recycler_id=recycler_id.strip(),
            full_name=full_name.strip(),
            id_number=id_number.strip(),
            email=email.strip(),
            phone=phone.strip(),
            district=district.strip(),
            registration_date=datetime.now().isoformat(),
            is_active=True
        )
        self._repository.add(recycler)
        return recycler

    def get_all_recyclers(self) -> list:
        return self._repository.get_all()

    def get_recycler_by_id(self, recycler_id: str) -> Recycler:
        self._validate_not_empty(recycler_id, "recycler_id")
        recycler = self._repository.get_by_id(recycler_id)
        if not recycler:
            raise ValueError(f"No se encontró ningún reciclador con el ID '{recycler_id}'.")
        return recycler

    def get_recyclers_by_district(self, district: str) -> list:
        self._validate_not_empty(district, "district")
        return [recycler for recycler in self._repository.get_all()
                if recycler.district.lower() == district.lower()]

    def set_active_status(self, recycler_id: str, is_active: bool) -> Recycler:
        recycler = self.get_recycler_by_id(recycler_id)
        recycler.is_active = is_active
        self._repository.add(recycler)
        return recycler