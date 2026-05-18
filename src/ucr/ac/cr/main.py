from src.ucr.ac.cr.repositories.recycler_repository import RecyclerRepository
from src.ucr.ac.cr.repositories.collection_point_repository import CollectionPointRepository
from src.ucr.ac.cr.repositories.record_repository import RecordRepository

from src.ucr.ac.cr.services.recycler_service import RecyclerService
from src.ucr.ac.cr.services.collection_point_service import CollectionPointService
from src.ucr.ac.cr.services.record_service import RecordService

from src.ucr.ac.cr.controllers.recycler_controller import RecyclerController
from src.ucr.ac.cr.controllers.collection_point_controller import CollectionPointController
from src.ucr.ac.cr.controllers.record_controller import RecordController

from src.ucr.ac.cr.views.login_view import LoginView
from src.ucr.ac.cr.views.main_app import MainApp


def main():
    # Layer 1 — Repositories
    recycler_repo = RecyclerRepository()
    point_repo = CollectionPointRepository()
    record_repo = RecordRepository()

    recycler_service = RecyclerService(recycler_repo)
    point_service = CollectionPointService(point_repo)
    record_service = RecordService(record_repo, recycler_service, point_service)

    recycler_controller = RecyclerController(recycler_service)
    point_controller = CollectionPointController(point_service)
    record_controller = RecordController(record_service)

    # abre la app principal después de un login exitoso
    def open_main_app():
        app = MainApp(recycler_controller, point_controller, record_controller)
        app.mainloop()

    # el login usa el mismo recycler_controller para validar credenciales
    login = LoginView(recycler_controller, on_login_success=open_main_app)
    login.mainloop()

if __name__ == "__main__":
    main()