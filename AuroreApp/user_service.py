import uuid
from AuroreApp.dataclasses.aurore_dataclasses import Hebergeur
from AuroreApp.models.sql_aurore import AuroreSQL

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
            if user.email == email:
                return user

    def add_user(self, user: User):
        self.users[user.id] = user


class SQLUserService(AbstractUserService):
    def __init__(self):
        pass

    def get_user_by_id(self, _id):
        with AuroreSQL() as client :
            user_list = client.get_table('HEBERGEUR')
            for user in user_list :
                if _id == user.id :
                    return user

    def get_user_by_email(self, email):
        with AuroreSQL() as client :
            user_list = client.get_table('HEBERGEUR')
            for user in user_list :
                if user.mail == email :
                    return user
        return None

    def add_user(self, user: User):
        with AuroreSQL() as client :
            new_user = Hebergeur(user.id,user.email,user.pwd,None,None,None,0)
            client.insert_object(new_user)