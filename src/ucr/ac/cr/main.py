from src.ucr.ac.cr.repositories.recycler_repository import RecyclerRepository
from src.ucr.ac.cr.repositories.collection_point_repository import CollectionPointRepository
from src.ucr.ac.cr.repositories.recycling_record_repository import RecyclingRecordRepository

from services.recycler_service import RecyclerService
from services.collection_point_service import CollectionPointService
from services.record_service import RecordService

from src.ucr.ac.cr.controllers.recycler_controller import RecyclerController
from src.ucr.ac.cr.controllers.collection_point_controller import CollectionPointController
from src.ucr.ac.cr.controllers.recycling_record_controller import RecyclingRecordController


# from src.ucr.ac.cr.views.main_view import MainView  cuando brayan haga la vista


def main():
    recycler_repo = RecyclerRepository("data/recyclers.json")
    point_repo = CollectionPointRepository("data/collection_points.json")
    record_repo = RecyclingRecordRepository("data/records.json")

    recycler_service = RecyclerService(recycler_repo)
    point_service = CollectionPointService(point_repo)

    record_service = RecordService(record_repo, recycler_repo, point_repo)

    recycler_controller = RecyclerController(recycler_service)
    point_controller = CollectionPointController(point_service)
    record_controller = RecyclingRecordController(record_service)

    # esto le toca a brayan
    # app = MainView(recycler_controller, point_controller, record_controller)
    # app.mainloop()


if __name__ == "__main__":
    main()