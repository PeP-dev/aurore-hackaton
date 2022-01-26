from AuroreApp import AuroreSQL
from AuroreApp import aurore_dataclasses
from AuroreApp.dataclasses.aurore_dataclasses import Conditions, Heberge,Logement
from dataclasses import dataclass

if __name__ == "__main__" :
    with AuroreSQL() as client :
        client.get_objects_from_table('CONDITIONS')