import geopandas
from Trajet import *
import ipywidgets as wid
from ipywidgets import interact
import pandas
import folium

_nantes = geopandas.read_file("244400404_adresses-postales-nantes-metropole.geojson")[["commune", "nom_voie", "numero_complet", "quartier", "lat", "long", "code_postal", "adresse"]]

def selection(commune = None, quartier = None, voie = None, numero = None, n = 10):
    results = _nantes.copy()
    if commune is not None:
        results = results[results["commune"] == commune]
    if quartier is not None:
        results = results[results["quartier"] == quartier]
    if voie is not None:
        results = results[results["nom_voie"] == voie]
    if numero is not None:
        results = results[results["numero_complet"] == numero]
    return results.sample(n=n)
from ipywidgets import interactive
from IPython.display import display

w_communes = wid.Dropdown(
    options = [("---", None)] + [(c, c) for c in sorted(_nantes.commune.unique())],
    description = "Commune",
    value = None
)

w_quartier = wid.Dropdown(
    options = [("---", None)],
    value = None,
    description = "Quartier"
)

w_voie = wid.Dropdown(
    options = [("---", None)],
    value = None,
    description = "Voie"
)

w_numéro = wid.Dropdown(
    options = [("---", None)],
    value = None,
    description = "Numéro"
)


def update_quartier(*args):
        filt = _nantes[_nantes["commune"] == w_communes.value]
        quartiers = sorted(filt.quartier.dropna().unique())
        w_quartier.options = [("---", None)] + [(q, q) for q in quartiers]
        w_quartier.value = None
        voies = sorted(filt.nom_voie.dropna().unique())
        w_voie.options = [("---", None)] + [(v,v) for v in voies]
        w_voie.value = None
        
w_communes.observe(update_quartier, names = "value")

def update_voie(*args):
    filt = _nantes[(_nantes["commune"] == w_communes.value) & (_nantes["quartier"] == w_quartier.value)]    
    voies = sorted(filt.nom_voie.dropna().unique())
    w_voie.options = [("---", None)] + [(v,v) for v in voies]
    w_voie.value = None


w_quartier.observe(update_voie, names = "value")

def update_numéro(*args):
    filt = _nantes[(_nantes["commune"] == w_communes.value) & (_nantes["quartier"] == w_quartier.value) & (_nantes["nom_voie"] == w_voie.value)]
    numéros = sorted(filt.numero_complet.dropna().unique())
    w_numéro.options = [("---", None)] + [(n,n) for n in numéros]
    w_numéro.value = None

w_voie.observe(update_numéro, names = "value")

w_nombre_patients = wid.BoundedIntText(
    description = "Nombre d'adresses",
    min = 1,
    max = 100,
    value = 10,
    step = 1,
    style = {"description_width": "initial"}
)

w_adresse = wid.VBox([
    wid.HBox([w_communes, w_quartier, w_voie, w_numéro]),
    w_nombre_patients]
    )

def sélection_interactive():
    return selection(commune = w_communes.value,
                     quartier = w_quartier.value,
                     voie = w_voie.value,
                     numero = w_numéro.value,
                     n = w_nombre_patients.value
                    )


def combine(*dfs):
    return pandas.concat(dfs)

def carte_adresses(df):
    centre_nantes = [47.2184, -1.5536]
    m = folium.Map(
        location=centre_nantes,
        zoom_start=12
    )
    infirm = True 
    for _, data in df.iterrows():
        if infirm:
            folium.Marker(
                location = [data.lat, data.long],
                tooltip = "Click me!",
                popup = "Infirmière",
                icon=folium.Icon(color="blue", icon="user-md", prefix="fa")
            ).add_to(m)
            infirm = False 
        else:
            folium.Marker(
                location=[data.lat, data.long],
                tooltip="Click me!",
                popup="Patient",
                icon=folium.Icon(color="red", icon="user", prefix="fa"),
            ).add_to(m)
    return m


