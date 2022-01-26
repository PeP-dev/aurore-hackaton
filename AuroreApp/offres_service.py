from datetime import datetime, timedelta


class Offre:
    def __init__(self, debut: datetime, fin: datetime, adresse: str, nbCouchages: int, description: str, tel):
        self.debut = debut
        self.fin = fin
        self.nbCouchages = nbCouchages
        self.description = description
        self.adresse = adresse
        self.tel = tel


class AbstractOffreService():
    def get_all(self):
        raise Exception("not implemented")

    def get_unchecked(self):
        raise Exception("not implemented")


class MockOffreService(AbstractOffreService):
    def __init__(self):
        self.offres = [
            Offre(datetime.now() - timedelta(days=3), datetime.now() + timedelta(days=3), "St Jo la street", 5,
                  "Description de la première maison", "0215452345"),
            Offre(datetime.now() + timedelta(days=1), datetime.now() + timedelta(days=5), "Commerce mais pas après 23h",
                  5, "Description de la 2e maison", "0654214578"),
            Offre(datetime.now() + timedelta(days=20), datetime.now() + timedelta(days=25), "La beaujoire", 5,
                  "Description de la 3e maison", "0254785421"),
        ]
        self.unchecked = [
            Offre(datetime.now() - timedelta(days=3), datetime.now() + timedelta(days=3), "St Jo la street", 5,
                  "Description de la première maison", "0215452345"),
            Offre(datetime.now() + timedelta(days=1), datetime.now() + timedelta(days=5), "Commerce mais pas après 23h",
                  5, "Description de la 2e maison", "0654214578"),
            Offre(datetime.now() + timedelta(days=20), datetime.now() + timedelta(days=25), "La beaujoire", 5,
                  "Description de la 3e maison", "0254785421"),
        ]

    def get_all(self):
        return self.offres

    def get_unchecked(self):
        return self.unchecked
