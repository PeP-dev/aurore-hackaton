from dataclasses import dataclass
import dataclasses
from sqlite3 import Date

class AuroreClass():
    def get_class_name(self):
        return self.__class__.__name__
    def get_attr_names(self):
        return self.__dict__.keys()
    def get_attr_values(self):
        return self.__dict__.values

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
class Condition(AuroreClass):
    id:int
    libelle:str

@dataclass
class Admin(AuroreClass):
    id:int
    login:str
    password:str

if __name__ == "__main__" :
    a = Admin(1,'oui','oui')