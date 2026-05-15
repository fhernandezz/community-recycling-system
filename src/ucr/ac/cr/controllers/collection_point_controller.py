class CollectionPointController:

    def __init__(self, service):
        self.service = service

    def create_point(self, point):
        return self.service.create_point(point)

    def get_points(self):
        return self.service.get_points()