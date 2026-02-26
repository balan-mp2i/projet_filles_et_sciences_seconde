import random as rd
import numpy as np
from faker import Faker

Identifiant = str
Latitude = float
Longitude = float
Trajet = list[Identifiant]

INFIRMIÈRE = "infirmière"


class Patient:
    def __init__(self, identifiant, latitude, longitude):
        self.identifiant = identifiant 
        self.latitude = latitude
        self.longitude = longitude


    def __repr__(self):
        return f"{self.identifiant}.\nCoordonnées:\n  Latitude : {self.latitude}\n  Longitude : {self.longitude}\n\n"


class Données:
    def __init__(self, données: dict[Identifiant, Patient]):
        self.données = données
        
    def coordonnées(self, patient: Identifiant) -> tuple[Latitude, Longitude]:
        return (self.données[patient].latitude, self.données[patient].longitude)


    def nombre_patients(self):
        return len(self.données.keys())-1

    def __repr__(self):
        return f"{self.données.values()}"

    # def reset(self):
    #     for p in self.données:
    #         if p != INFIRMIÈRE:
    #             self.données[p].vu = False


def données_aléatoires(N=10):
        fake = Faker('fr_FR')
        ids = [fake.name() for _ in range(N)]
        lat = [47.194704 + (47.309310 - 47.194704) * rd.random() for _ in range(N)]
        lon = [-1.723280 + (-1.381573 + 1.723280) * rd.random() for _ in range(N)]
        patients = {INFIRMIÈRE: Patient(INFIRMIÈRE, 47.297043, -1.445224)}
        for i in range(N):
            patients[ids[i]] = Patient(ids[i],lat[i], lon[i] )
        
        return Données(patients)

#### DONNÉES #####
#
#Les méthodes ci-dessous agissent sur les données.
#
# 




données_test = Données({INFIRMIÈRE: Patient("infirmière", 47.21811, -1.55448),
            "Marcel": Patient("Marcel", 47.204644, -1.559530),
            "Françoise": Patient("Françoise", 47.212327, -1.560366),
            "Timéo": Patient("Timéo", 47.214880, -1.534665)
        })




#### TRAJET ####
#
#
# 
class Trajet:
    def __init__(self, données: Données):
        self.trajet = [INFIRMIÈRE, INFIRMIÈRE]
        self.données = données
        self.patients = {p.identifiant: False for p in données.données.values()}
        self.patients[INFIRMIÈRE] = True 

    def insère_patient(self, patient: Identifiant):
        self.trajet.insert(-1, patient)
        self.patients[patient] = True

    def patients_à_visiter(self) -> None:
        ps = [p  for p in self.patients if not self.patients[p]]
        print("Patients à voir : ")
        for p in ps:
            print("-", p)

    def patient_aléatoire(self) -> Identifiant:
        return rd.choice([p for p in self.patients if not self.patients[p]])

    def patient(self, i):
        return self.trajet[i]

    def échange(self, patient1, patient2) -> Trajet:
        t = Trajet(self.données)
        tr = []
        t.trajet = tr
        for p in self.trajet:
            if p not in [patient1, patient2]:
                tr.append(p)
            elif p == patient1:
                tr.append(patient2)
            elif p == patient2:
                tr.append(patient1)
        return t

    def plus_proche_patient(self) -> Identifiant:
        localisation = self.trajet[-2]
        return min([p for p in self.patients if not self.patients[p]], key = lambda p: _distance(self.données, localisation, p))
        
    def __repr__(self):
        return " -> ".join(self.trajet)
    
def _distance(données: Données, source: Identifiant, cible: Identifiant) -> float:
    (phi_a, lambda_a) = données.coordonnées(source)
    (phi_b, lambda_b) = données.coordonnées(cible)
    x = phi_b - phi_a
    y = (lambda_b - lambda_a) * np.cos(np.radians((phi_a + phi_b)/2))
    return 1.852 * 60 * np.sqrt(x**2 + y**2)

class Algorithmes:
    def __init__(self):
        self.algos = {}
    def ajout_algo(self, fonction, nom):
        self.algos[nom] = fonction

class Jeux:
    def __init__(self):
        self.jeux = {}
    def ajout_données(self, adresses, nom):
        fake = Faker('fr_FR')
        données = {}
        infirm = True 
        for _, d in adresses.iterrows():
            if infirm:
                données["infirmière"] = Patient("infirmière", d.lat, d.long)
                infirm = False
            else:
                p = fake.name()
                données[p] = Patient(p, d.lat, d.long)
        self.jeux[nom] = Données(données)
