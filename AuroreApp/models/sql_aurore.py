from sqlparse import sql
from AuroreApp.dataclasses.aurore_dataclasses import AuroreClass, Conditions, Heberge, Hebergeur, Logement
import AuroreApp.models.sql_request as sql_request
import os

#En attendant-------
os.environ['HOST'] = 'localhost'
os.environ['DATABASE'] = 'aurore'
os.environ['USER'] = 'root'
os.environ['PASSwORD'] = 'root'
#-------------------

keys = os.environ
HOST,DATABASE,USER,PASSWORD = keys['HOST'],keys['DATABASE'],keys['USER'],keys['PASSWORD']

class AuroreSQL(sql_request.Client):

    SET_TABLES_CLASS= {Conditions,Logement,Heberge,Hebergeur}
    DICT_TABLES_NAME = {a.__name__.upper():a for a in SET_TABLES_CLASS}
    DICT_TABLES_CLASS = {a:a.__name__.upper() for a in SET_TABLES_CLASS}

    def __init__(self) -> None:
        super().__init__(host=HOST,database=DATABASE,user=USER,password=PASSWORD)

    #TESTEURS
    def test_object_in_table(self,objet):
        if objet.__class__ not in AuroreSQL.SET_TABLES_CLASS :
            raise KeyError(f"La table associé à l'objet {objet} n'existe pas")
    
    def test_name_is_table(self,table_name:str):
        if table_name.upper() not in AuroreSQL.DICT_TABLES_NAME :
            raise KeyError(f"La table {table_name} n'existe pas")

    #INSERTION/DELETION
    def insert_object(self,objet:AuroreClass):
        self.test_object_in_table(objet)
        #Génération du texte de requête sql
        sql_string = self.fast_insert(objet.get_table_name(),objet.get_attr_names(),objet.get_attr_values())
        self.process_send(sql_string)
    
    def delete_on_pk(self,table:str,pkey_name,pkey):
        sql_string = self.fast_delete_on_pk(table,pkey_name,pkey)
        self.process_send(sql_string)

    #GETTERS
    def get_objects_from_table(self,table_name:str)->AuroreClass:
        self.test_name_is_table(table_name)
        
        #Récupération des attributs de classe (et donc table) pour la requête
        classe = AuroreSQL.DICT_TABLES_NAME[table_name]
        args = classe.__dict__['__match_args__']
        names = ""
        for a in args :
            names += a + ","
        names = names[:-1]

        #Requête
        sql_list = self.get_table(table_name,filter=names)

        #Création de la liste des objets de retour
        res_liste = []

        for sql_result in sql_list :
            #Création du dictionnaire attribut:valeur propre à la classe
            attributs = {}
            print(args)
            print(sql_list)
            for i in range(len(args)):
                attributs[args[i]] = sql_result[i]

            res_liste.append(classe(**attributs))

        return res_liste
                
            
        """
        res_list = []
        for res in sql_list :
            res_list.append(classe())"""
        

        
        


    
