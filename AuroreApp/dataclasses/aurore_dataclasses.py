from dataclasses import dataclass
from sqlite3 import Date

class AuroreClass():
    def get_table_name(self):
        return self.__class__.__name__.upper()
    def get_attr_names(self):
        return list(self.__dict__.keys())
    def get_attr_values(self):
        return list(self.__dict__.values())

@dataclass
class Hebergeur(AuroreClass):
    id:int
    login:str
    password:str
    nom:str

@dataclass
class Logement(AuroreClass):
    id:int
    debut:Date
    fin:Date
    adresse:str
    tel:str

@dataclass
class Heberge(AuroreClass):
    id:int
    nom:str
    prenom:str
    tel:str

@dataclass
class Conditions(AuroreClass):
    id:int
    libelle:str

@dataclass
class Admin(AuroreClass):
    id:int
    login:str
    password:str

if __name__ == "__main__" :
    a = Admin(1,'oui','oui')