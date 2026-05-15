class DeliveryController:

    def __init__(self, service):
        self.service = service

    def create_delivery(self, delivery):
        return self.service.create_delivery(delivery)

    def get_deliveries(self):
        return self.service.get_deliveries()