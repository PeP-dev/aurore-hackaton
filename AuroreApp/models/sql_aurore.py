from sqlparse import sql
from AuroreApp.dataclasses.aurore_dataclasses import *
import AuroreApp.models.sql_request as sql_request
import os

HOST, DATABASE, USER, PASSWORD = os.getenv('HOST'), os.getenv('DATABASE'), os.getenv('USER'), os.getenv('PASSWORD')


class AuroreSQL(sql_request.Client):
    SET_TABLES_CLASS = {CondLogement, Logement, Heberge, Hebergeur}
    DICT_TABLES_NAME = {a.__name__.upper(): a for a in SET_TABLES_CLASS}
    DICT_TABLES_CLASS = {a: a.__name__.upper() for a in SET_TABLES_CLASS}

    def __init__(self) -> None:
        super().__init__(host=HOST, database=DATABASE, user=USER, password=PASSWORD)

    # TESTEURS
    def test_object_in_table(self, objet):
        if objet.__class__ not in AuroreSQL.SET_TABLES_CLASS:
            raise KeyError(f"La table associé à l'objet {objet} n'existe pas")

    def test_name_is_table(self, table_name: str):
        if table_name.upper() not in AuroreSQL.DICT_TABLES_NAME:
            raise KeyError(f"La table {table_name} n'existe pas")

    # INSERTION/DELETION
    def insert_object(self, objet: AuroreClass):
        self.test_object_in_table(objet)
        # Génération du texte de requête sql
        sql_string = self.fast_insert(objet.get_table_name(), objet.get_attr_names(), objet.get_attr_values())
        self.process_send(sql_string)

    def delete_on_pk(self, table: str, pkey_name, pkey):
        sql_string = self.fast_delete_on_pk(table, pkey_name, pkey)
        self.process_send(sql_string)

    # GETTERS
    def get_objects_from_table(self, table_name: str) -> list:
        table_name = table_name.upper()
        self.test_name_is_table(table_name)

        # Récupération des attributs de classe (et donc table) pour la requête
        classe = AuroreSQL.DICT_TABLES_NAME[table_name]
        args = classe.__dict__['__match_args__']
        names = ""
        for a in args:
            names += a + ","
        names = names[:-1]

        # Requête
        sql_list = self.get_table(table_name, filter=names)

        # Création de la liste des objets de retour
        res_liste = []

        for sql_result in sql_list:
            # Création du dictionnaire attribut:valeur propre à la classe
            attributs = {}
            for i in range(len(args)):
                attributs[args[i]] = sql_result[i]

            res_liste.append(classe(**attributs))

        return res_liste

    # SERVICES
    def is_admin(self,_id):
        user_list:list = self.get_objects_from_table('HEBERGEUR')
        filter_by_id = [i for i in user_list if (i.id == _id)]
        length = len(filter_by_id)
        
        match length :
            case 0 :
                raise KeyError(f"No references found for id={_id}")
            case 1 :
                return filter_by_id[0].is_admin
            case _ :
                raise KeyError(f"Multiple references found for id={_id} : {filter_by_id}")

    


    
