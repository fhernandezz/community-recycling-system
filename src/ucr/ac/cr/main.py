from src.ucr.ac.cr.repositories.recycler_repository import RecyclerRepository
from src.ucr.ac.cr.repositories.collection_point_repository import CollectionPointRepository
from src.ucr.ac.cr.repositories.record_repository import RecordRepository

from src.ucr.ac.cr.services.recycler_service import RecyclerService
from src.ucr.ac.cr.services.collection_point_service import CollectionPointService
from src.ucr.ac.cr.services.record_service import RecordService

from src.ucr.ac.cr.controllers.recycler_controller import RecyclerController
from src.ucr.ac.cr.controllers.collection_point_controller import CollectionPointController
from src.ucr.ac.cr.controllers.record_controller import RecordController


def main():
    recycler_repo = RecyclerRepository("data/recyclers.json")
    point_repo = CollectionPointRepository("data/collection_points.json")
    record_repo = RecordRepository("data/records.json")

    recycler_service = RecyclerService(recycler_repo)
    point_service = CollectionPointService(point_repo)
    record_service = RecordService(record_repo, recycler_service, point_service)

    recycler_controller = RecyclerController(recycler_service)
    point_controller = CollectionPointController(point_service)
    record_controller = RecordController(record_service)

if __name__ == "__main__":
    main()