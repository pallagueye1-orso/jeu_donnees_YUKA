import pandas as pd
from statsmodels.miscmodels.ordinal_model import OrderedModel

# Charger les données
df = pd.read_csv('../data/jeu_donnees_yuka.csv', sep=';')
print(df.head())
print(df.columns)

# Variable dépendante (ordonnée)
y = df['score_yuka_ordonne']

# -------------------------
# MODELE 1 : COMPLET (SATURÉ)
# -------------------------
X1 = df[['graisses_saturees_100g',
         'sel_100g',
         'fibres_100g',
         'proteines_100g',
         'nb_additifs',
         'bio',
         'ultra_transforme']]

model1 = OrderedModel(y, X1, distr='logit')
res1 = model1.fit(method='bfgs')
print("\n=== MODELE 1 : COMPLET ===")
print(res1.summary())

# -------------------------
# MODELE 2 : SANS VARIABLES QUALITATIVES
# -------------------------
X2 = df[['graisses_saturees_100g',
         'sel_100g',
         'fibres_100g',
         'proteines_100g']]

model2 = OrderedModel(y, X2, distr='logit')
res2 = model2.fit(method='bfgs')
print("\n=== MODELE 2 : NUTRITION SEULE ===")
print(res2.summary())

# -------------------------
# MODELE 3 : SANS ADDITIFS ET ULTRA-TRANSFORMÉ
# -------------------------
X3 = df[['graisses_saturees_100g',
         'sel_100g',
         'fibres_100g',
         'proteines_100g',
         'bio']]

model3 = OrderedModel(y, X3, distr='logit')
res3 = model3.fit(method='bfgs')
print("\n=== MODELE 3 : SANS ULTRA-TRANSFORMÉ ===")
print(res3.summary())

# -------------------------
# SAUVEGARDE DES RESULTATS
# -------------------------
with open('../resultats_havar.txt', 'w') as f:
    f.write("=== MODELE 1 ===\n")
    f.write(res1.summary().as_text())
    f.write("\n\n=== MODELE 2 ===\n")
    f.write(res2.summary().as_text())
    f.write("\n\n=== MODELE 3 ===\n")
    f.write(res3.summary().as_text())
