from AuroreApp import AuroreSQL
from AuroreApp.dataclasses.aurore_dataclasses import *
from dataclasses import dataclass

if __name__ == "__main__" :
    add = True
    delete = True
    with AuroreSQL() as client :
        
        if delete :
            client.TruncateAll('aurore')
        
        if add :
            heberge = Heberge(1,'Marc','Carm','0651428688')
            condition = CondLogement(3,1,'Non fumeur')
            hebergeur = Hebergeur(1,'Michèle','Tu connais','michele@gmail.com','ouaf','0651428688',1)
            hebergeur2 = Hebergeur(2,'Michèle','Pain','michele.pain@gmail.com','ouaf2','0651428658',0)

            client.insert_objects([heberge,condition,hebergeur,hebergeur2])


        print(
            client.get_objects_from_table('CONDLOGEMENT'),
            client.get_objects_from_table('HEBERGE'),
            client.get_objects_from_table('HEBERGEUR')
            )
        
        print(
            #This should return false/0
            client.is_admin(2), "<-- should be 0\n",
            #This one should return true/1
            client.is_admin(1), "<-- should be 1"
        )