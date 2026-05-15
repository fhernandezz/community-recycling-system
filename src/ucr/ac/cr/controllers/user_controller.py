class UserController:

    def __init__(self, service):
        self.service = service

    def create_user(self, user):
        return self.service.create_user(user)

    def get_users(self):
        return self.service.get_users()