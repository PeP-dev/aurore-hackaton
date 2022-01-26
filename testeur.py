from typing import Container
from AuroreApp import AuroreSQL
from AuroreApp import aurore_dataclasses
from AuroreApp.dataclasses.aurore_dataclasses import Conditions, Heberge,Logement
from dataclasses import dataclass

if __name__ == "__main__" :
    add = True
    delete = True
    with AuroreSQL() as client :
        
        if delete :
            client.TruncateAll('aurore')
        
        if add :
            heberge = Heberge(1,'Marc','Carm','0651428688')
            condition = Conditions(3,'Non fumeur')

            client.insert_object(heberge)
            client.insert_object(condition)


        print(
            client.get_objects_from_table('CONDITIONS'),
            client.get_objects_from_table('HEBERGE')
            )