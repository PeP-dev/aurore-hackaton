import sql_request
import os
import time

os.environ['HOST'] = 'localhost'
os.environ['DATABASE'] = 'aurore'
os.environ['USER'] = 'root'
os.environ['PASSwORD'] = 'root'

keys = os.environ
HOST,DATABASE,USER,PASSWORD = keys['HOST'],keys['DATABASE'],keys['USER'],keys['PASSWORD']

class AuroreSQL(sql_request.Client):

    TABLES = {
        'HEBERGES': {'id','nom','prenom','tel','mail'},
        'ADMIN': {'id','login','password'},
        'HEBERGEURS':{'id','login','password','nom'},
        'LOGEMENTS':{'debut','fin','adresse','tel','mail'},
        'CONDITIONS':{'id','libelle'}
    }

    def __init__(self) -> None:
        super().__init__(host=HOST,database=DATABASE,user=USER,password=PASSWORD)
    
    def check(self,table:str,kwargs:dict) :
        if table in AuroreSQL.TABLES :
            if len(kwargs) != len(AuroreSQL.TABLES[table]) :
                raise KeyError(f"Les données fournies ne correspondent pas aux attributs de la table {table}. Données : {kwargs} \n Données attendues : {AuroreSQL.TABLES[table]}")
            for kwarg in kwargs :
                if not(kwarg in AuroreSQL.TABLES[table]) :
                    raise KeyError(f"Les données fournies ne correspondent pas aux attributs de la table {table}. Données : {kwargs} \n Données attendues : {AuroreSQL.TABLES[table]}")
        else :
            raise KeyError(f"La table {table} n'existe pas")

    def insert(self,table:str,**kwargs):
        self.check(table,kwargs)
        liste = [(a,kwargs[a]) for a in kwargs]
        names = [a[0] for a in liste]
        values = [a[1] for a in liste]
        sql_string = self.fast_insert(table,names,values)
        self.process_send(sql_string)
    
    def delete(self,table:str,pkey_name,pkey):
        sql_string = self.fast_delete_on_pk(table,pkey_name,pkey)
        self.process_send(sql_string)

    
if __name__ == "__main__" :
    with AuroreSQL() as client :
        client.insert('CONDITIONS',id=1,libelle='oui')