from AuroreApp.dataclasses.aurore_dataclasses import AuroreClass, Condition, Heberge, Hebergeur, Logement
import sql_request
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

    TABLES = {Condition,Logement,Heberge,Hebergeur}

    def __init__(self) -> None:
        super().__init__(host=HOST,database=DATABASE,user=USER,password=PASSWORD)
    
    def insert(self,objet:AuroreClass):
        if objet not in AuroreSQL.TABLES :
            raise KeyError(f"La table associé à l'objet {objet} n'existe pas")

        #Génération du texte de requête sql
        sql_string = self.fast_insert(objet.get_class_name,objet.get_attr_names,objet.get_attr_values)
        self.process_send(sql_string)
    
    def delete_on_pk(self,table:str,pkey_name,pkey):
        sql_string = self.fast_delete_on_pk(table,pkey_name,pkey)
        self.process_send(sql_string)

    
if __name__ == "__main__" :
    with AuroreSQL() as client :
        client.insert('CONDITIONS',id=1,libelle='oui')