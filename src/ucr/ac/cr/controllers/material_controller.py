class MaterialController:

    def __init__(self, service):
        self.service = service

    def create_material(self, material):
        return self.service.create_material(material)

    def get_materials(self):
        return self.service.get_materials()