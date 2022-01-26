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
    
    def del_user(self, user:User):
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
    
    def del_user(self,user:User):
        self.users.__delitem__(user.id)
    


class SQLUserService(AbstractUserService):
    def __init__(self):
        pass

    def get_user_by_id(self, _id)->Hebergeur:
        with AuroreSQL() as client :
            user_list = client.get_objects_from_table('HEBERGEUR')
            for user in user_list :
                if _id == user.id :
                    return user

    def get_user_by_email(self, email)->Hebergeur:
        with AuroreSQL() as client :
            user_list = client.get_objects_from_table('HEBERGEUR')
            for user in user_list :
                if user.mail == email :
                    return user
        return None

    def add_user(self, user: Hebergeur)->None:
        with AuroreSQL() as client :
            client.insert_object(user)
    
    def add_user_more(self,_id,email,pwd,nom,prenom,tel,is_admin=0)->None :
        new_user = Hebergeur(_id,email,pwd,nom,prenom,tel,is_admin)
        with AuroreSQL() as client :
            client.insert_object(new_user)
    
    def del_user(self,user:User)->None:
        if not(self.get_user_by_id(user.id) == None) :
            with AuroreSQL() as client :
                sql_text = client.fast_delete_on_pk('HEBERGEUR','id',user.id)
                client.process_send(sql_text)
