from src.ucr.ac.cr.repositories.recycler_repository import RecyclerRepository
from src.ucr.ac.cr.repositories.collection_point_repository import CollectionPointRepository
from src.ucr.ac.cr.repositories.record_repository import RecordRepository

from src.ucr.ac.cr.services.recycler_service import RecyclerService
from src.ucr.ac.cr.services.collection_point_service import CollectionPointService
from src.ucr.ac.cr.services.record_service import RecordService

from src.ucr.ac.cr.controllers.recycler_controller import RecyclerController
from src.ucr.ac.cr.controllers.collection_point_controller import CollectionPointController
from src.ucr.ac.cr.controllers.record_controller import RecordController

# from src.ucr.ac.cr.views.main_view import MainView  # le toca a Brayan


def main():
    """
    Entry point. Instantiates all layers bottom-up (DIP).
    No layer creates its own dependencies — everything is injected here.
    """

    # Layer 1 — Repositories (each loads its JSON once on __init__)
    recycler_repo = RecyclerRepository("data/recyclers.json")
    point_repo = CollectionPointRepository("data/collection_points.json")
    record_repo = RecordRepository("data/records.json")

    # Layer 2 — Services
    # RecordService receives the other two SERVICES, not their repos (DIP + ISP)
    recycler_service = RecyclerService(recycler_repo)
    point_service = CollectionPointService(point_repo)
    record_service = RecordService(record_repo, recycler_service, point_service)

    recycler_controller = RecyclerController(recycler_service)
    point_controller = CollectionPointController(point_service)
    record_controller = RecordController(record_service)

if __name__ == "__main__":
    main()