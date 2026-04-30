import pandas as pd
from statsmodels.miscmodels.ordinal_model import OrderedModel

# Charger données
df = pd.read_csv("../data/jeu_donnees_yuka.csv", sep=';')

print(df.head())
print(df.columns)

# Variable dépendante
y = df["score_yuka_ordonne"]

# Variables explicatives
X = df[[
    "calories_100g",
    "sucres_100g",
    "graisses_saturees_100g",
    "sel_100g",
    "fibres_100g",
    "proteines_100g",
    "nb_additifs",
    "bio",
    "ultra_transforme"
]]

# Modèle Ordered Logit
model = OrderedModel(y, X, distr='logit')

result = model.fit(method='bfgs')

print(result.summary())

with open("../resultats_havar.txt", "w") as f:
    f.write(result.summary().as_text())