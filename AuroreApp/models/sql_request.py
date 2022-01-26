import mysql.connector
from mysql.connector.errors import Error,IntegrityError
import sqlparse

global_pretify = True
global_echo_connection = True

class Client(object):
       
    def __init__(self,host='localhost',database='data_leaderboard', user='root',password='root'):
        self.connection = mysql.connector.connect(host=host,database=database,user=user,password=password)
        self.host = host
        self.database = database
        
        if self.connection.is_connected():
            db_Info = self.connection.get_server_info()
            if global_echo_connection :
                print("Connected to MySQL Server version ", db_Info)
            self.cursor = self.connection.cursor()

    def close(self):
        self.connection.close()

    def pretify_sql(self,sql):
        print("\n--------------REQUEST----------------")
        print(sqlparse.format(sql, reindent=True, keyword_case='upper'))
        print("--------------------------------------\n")
        return

    def formatage_string(self,string:str)->str:
        string = string.replace("'",r"\'")
        string = "\'"+string+"\'"
        return string

    #TRUNCATE
    def TruncateAll(self,database_name:str):
        self.cursor.execute(f"""
                SELECT
                    Concat('TRUNCATE TABLE ', TABLE_NAME)
                FROM
                    INFORMATION_SCHEMA.TABLES
                WHERE
                    table_schema = '{database_name}';
                """)
        records = self.cursor.fetchall()
        records = [("SET FOREIGN_KEY_CHECKS=0;",)] + records + [("SET FOREIGN_KEY_CHECKS=1;",)]
        for request in records :
            self.cursor.execute(request[0])
        self.connection.commit()
        print(f"All tables from {database_name} have been truncated")

    def process_send(self,sql,pretify=global_pretify) :
        if pretify :
            self.pretify_sql(sql)
        self.cursor.execute(sql)
        self.connection.commit()
        #self.connection.close()
        return
    def process_get(self,sql,pretify=global_pretify) :
        if pretify :
            self.pretify_sql(sql)
        self.cursor.execute(sql)
        records = self.cursor.fetchall()
        #self.connection.close()
        return records
    
    #Ecriture SQL
    def fast_delete_on_pk(self,table:str,pk_name,pk):
        if type(pk) == str :
            pk = self.formatage_string(pk)
        sql = f"DELETE FROM {table} WHERE {pk_name} = {pk}"
        return sql
    def fast_insert(self,table:str,names:list[str],values:list) :
        colonnes = names.__str__()[1:-1]
        colonnes = [i for i in colonnes if i!="\'"]
        colonnes = "(" + "".join(colonnes) + ")"
        #Délétions des espaces en trop
        for i,v in enumerate(values) :
            if type(v) == str :
                values [i] = v.strip()
                
        values = "(" + values.__str__()[1:-1] + ")"
        sql = f"INSERT INTO {table} {colonnes} VALUES {values}"
        return sql
    
    def get_table(self,table:str,filter="*"):
        sql = f"SELECT {filter} FROM {table}"
        return self.process_get(sql)
        
    #WITH SUPPORT
    def __enter__(self):
        return self
       
    def __exit__(self,type,value,traceback) :
        if global_echo_connection :
            print("Connexion closed")
        self.close()     

