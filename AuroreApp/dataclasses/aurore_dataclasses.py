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
    mail:str
    mdp:str
    nom:str=None
    prenom:str=None
    tel:str=None
    is_admin:int=0

@dataclass
class Logement(AuroreClass):
    id:int
    hebergeur_id:int
    nombre_place:int
    adresse:str

@dataclass
class Heberge(AuroreClass):
    id:int
    nom:str
    prenom:str
    infos:str

@dataclass
class CondLogement(AuroreClass):
    id:int
    logement_id:int
    libelle:str

if __name__ == "__main__" :
    pass