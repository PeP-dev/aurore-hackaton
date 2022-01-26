import uuid


class User:
    def __init__(self, id, identity, email, pwd, is_admin):
        self.id = id
        self.email = email
        self.pwd = pwd
        self.identity = identity
        self.is_admin = is_admin


class AbstractUserService:
    def get_user_by_id(self, id):
        raise Exception("Not implemented")

    def add_user(self, user: User):
        raise Exception("Not implemented")

    def get_user_by_email(self, email):
        raise Exception("Not implemented")


class MockUserService(AbstractUserService):
    def __init__(self):
        self.users = {}

    def get_user_by_id(self, id):
        if id in self.users:
            return self.users[id]

    def get_user_by_email(self, email):
        for user in self.users.values():
            print(user, email)
            if user.email == email:
                return user

    def add_user(self, user: User):
        self.users[user.id] = user
