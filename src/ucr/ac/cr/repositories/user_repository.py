import json
from models.user import User


class UserRepository:

    def __init__(self, file_path="data/users.json"):
        self.file_path = file_path

    def get_all(self):
        with open(self.file_path, "r") as file:
            data = json.load(file)

        return [User.from_dict(item) for item in data]

    def add(self, user: User):
        users = self.get_all()

        users.append(user)

        self.save_all(users)

    def save_all(self, users):
        with open(self.file_path, "w") as file:
            json.dump(
                [u.to_dict() for u in users],
                file,
                indent=4
            )