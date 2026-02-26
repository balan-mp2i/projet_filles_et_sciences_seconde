from Trajet import *
import ipywidgets as wid


def _distance_totale(trajet):
    return sum(distance(trajet.données, trajet.patient(i), trajet.patient(i+1)) for i in range(len(trajet.trajet)-1))

def trajet_ordre(données): #le trajet visite les patients dans l'ordre donné par données
    t = Trajet(données)
    for p in t.patients:
        print(f"ajout de {p}")
        if p != "infirmière":
            t.insère_patient(p)
            print(f"distance totale : {_distance_totale(t)}")
    return t
    
def trajet_inverse(données): #le trajet dans le sens inverse de l'ordre donné par données
    t = Trajet(données)
    for p in t.patients:
        if p != "infirmière":
            t.insère_patient(p)
    return t

class Options():
    def __init__(self, jeux={}, algo={}):
        self.jeux = jeux
        self.algo = algo 
    def ajout_données(self, données, nom):
        self.jeux[nom] = données
    def ajout_algo(self, algo, nom):
        self.algo[nom] = algo
    def jeux_de_données(self):
        return [(nom, données) for nom, données in self.jeux.items()]
    def algorithmes(self):
        return [(nom, algo) for nom, algo in self.algo.items()]

options_bidon = Options()
for n in [10, 15, 20]:
    options_bidon.ajout_données(données_aléatoires(n), f"données aléatoires à {n} patients")
options_bidon.ajout_algo(trajet_ordre, "trajet dans l'ordre")
options_bidon.ajout_algo(trajet_inverse, "trajet dans l'ordre inverse")




def distance(données: Données, source: Identifiant, cible: Identifiant) -> float:
    (phi_a, lambda_a) = données.coordonnées(source)
    (phi_b, lambda_b) = données.coordonnées(cible)
    x = phi_b - phi_a
    y = (lambda_b - lambda_a) * np.cos(np.radians((phi_a + phi_b)/2))
    return 1.852 * 60 * np.sqrt(x**2 + y**2)




def longueurs(trajet):
    n = len(trajet.trajet)
    return [distance(trajet.données, trajet.patient(i), trajet.patient(i+1)) for i in range(n-1)]

import folium



def tracé(trajet, couleur_icone_infirmiere="blue", couleur_icones_patients="red", couleur_segments_trajet=["yellow", "yellow"]):
    données = trajet.données
    centre_nantes = [47.2184, -1.5536]
    m = folium.Map(
        location=centre_nantes,
        zoom_start=12
    )
    for patient in données.données:
        if patient == "infirmière":
            folium.Marker(
                location = données.coordonnées(patient),
                tooltip = "Click me!",
                popup = "Infirmière",
                icon=folium.Icon(color=couleur_icone_infirmiere, icon="user-md", prefix="fa")
            ).add_to(m)
            infirm = False 
        else:
            folium.Marker(
                location=données.coordonnées(patient),
                tooltip="Click me!",
                popup="Patient",
                icon=folium.Icon(color=couleur_icones_patients, icon="user", prefix="fa"),
            ).add_to(m)
    folium.ColorLine(positions = [données.coordonnées(p) for p in trajet.trajet],
                     colors = longueurs(trajet), 
                     colormap = couleur_segments_trajet,
                     weight = 1
                    ).add_to(m)
    return m

bouton = wid.Button(
    description = "Afficher la carte"
)


def on_click(b):
    with out:
        out.clear_output()
        trajet = tournée()
    with carte:
        carte.clear_output(wait=True)
        m = tracé(trajet)
        display(m)
        

bouton.on_click(on_click)
