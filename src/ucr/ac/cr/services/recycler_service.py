from datetime import datetime
from src.ucr.ac.cr.models.recycler import Recycler


class RecyclerService:
    """
    Servicio encargado de la gestión de recicladores.

    Responsabilidades:
    - Registro de recicladores
    - Validaciones de identidad y datos
    - Consultas por ID y distrito
    - Gestión de estado activo/inactivo

    Actúa como capa de lógica de negocio entre repositorio y modelo.
    """

    def __init__(self, repository):
        """
        Inicializa el servicio con su repositorio.

        Args:
            repository: Repositorio de recicladores.
        """
        self._repository = repository

    def _validate_not_empty(self, value: str, field_name: str) -> None:
        """
        Valida que un campo obligatorio no esté vacío.
        """
        if not value or not str(value).strip():
            raise ValueError(f"El campo '{field_name}' no puede estar vacío.")

    def _validate_email_format(self, email: str) -> None:
        """
        Valida formato básico de correo electrónico.
        """
        if "@" not in email:
            raise ValueError(f"El correo '{email}' no tiene un formato válido.")

    def _validate_id_number_unique(self, id_number: str) -> None:
        """
        Verifica que la cédula no esté registrada previamente.
        """
        for existing_recycler in self._repository.get_all():
            if existing_recycler.id_number == id_number:
                raise ValueError(
                    f"Ya existe un reciclador registrado con la cédula '{id_number}'."
                )

    def _validate_recycler_id_unique(self, recycler_id: str) -> None:
        """
        Verifica que el ID del reciclador no exista previamente.
        """
        for existing_recycler in self._repository.get_all():
            if existing_recycler.recycler_id == recycler_id:
                raise ValueError(
                    f"El ID de reciclador '{recycler_id}' ya existe."
                )

    def register_recycler(self, recycler_id: str, full_name: str, id_number: str,
                          email: str, phone: str, district: str) -> Recycler:
        """
        Registra un nuevo reciclador en el sistema.

        Incluye validaciones de:
        - Campos obligatorios
        - Formato de email
        - Unicidad de ID y cédula

        Retorna:
            Recycler: objeto creado y almacenado.
        """
        self._validate_not_empty(recycler_id, "recycler_id")
        self._validate_not_empty(full_name, "full_name")
        self._validate_not_empty(id_number, "id_number")
        self._validate_not_empty(email, "email")
        self._validate_not_empty(phone, "phone")
        self._validate_not_empty(district, "district")

        self._validate_email_format(email)
        self._validate_recycler_id_unique(recycler_id)
        self._validate_id_number_unique(id_number)

        new_recycler = Recycler(
            recycler_id=recycler_id.strip(),
            full_name=full_name.strip(),
            id_number=id_number.strip(),
            email=email.strip(),
            phone=phone.strip(),
            district=district.strip(),
            registration_date=datetime.now().isoformat(),
            is_active=True
        )

        self._repository.add(new_recycler)
        return new_recycler

    def get_all_recyclers(self) -> list:
        """Retorna todos los recicladores registrados."""
        return self._repository.get_all()

    def get_recycler_by_id(self, recycler_id: str) -> Recycler:
        """
        Obtiene un reciclador por su ID.

        Lanza error si no existe.
        """
        self._validate_not_empty(recycler_id, "recycler_id")

        found_recycler = self._repository.get_by_id(recycler_id)

        if not found_recycler:
            raise ValueError(
                f"No se encontró ningún reciclador con el ID '{recycler_id}'."
            )

        return found_recycler

    def get_recyclers_by_district(self, district: str) -> list:
        """
        Filtra recicladores por distrito (case-insensitive).
        """
        self._validate_not_empty(district, "district")

        return [
            existing_recycler
            for existing_recycler in self._repository.get_all()
            if existing_recycler.district.lower() == district.lower()
        ]

    def set_active_status(self, recycler_id: str, is_active: bool) -> Recycler:
        """
        Cambia el estado activo/inactivo de un reciclador.
        """
        recycler_to_update = self.get_recycler_by_id(recycler_id)
        recycler_to_update.is_active = is_active

        self._repository.update(recycler_to_update)
        return recycler_to_update