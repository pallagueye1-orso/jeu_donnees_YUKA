# Projet Économétrie Qualitative — Modélisation des notations Yuka
 
**Master 1 BIDABI — Université Sorbonne Paris Nord**  
**Cours : Économétrie qualitative**  
**Groupe :** Havar Baskara · Mouhammad Gaye · Palla Gueye
 
---
 
## Contexte
 
Ce projet analyse les facteurs qui expliquent la notation Yuka des produits alimentaires.
Yuka est une application qui évalue la qualité nutritionnelle des produits selon une échelle ordonnée :
Mauvais → Médiocre → Bon → Excellent.
 
L'objectif est d'identifier et d'estimer un modèle économétrique permettant d'expliquer
cette notation à partir de la composition nutritionnelle des produits.
 
---
 
## Données
 
**Fichier :** `data/jeu_donnees_yuka.csv`  
**Observations :** 1 000 produits alimentaires  
**Valeurs manquantes :** aucune
 
### Variables
 
| Variable | Type | Description |
|---|---|---|
| `score_yuka_ordonne` | Ordonnée (1→4) | **Variable dépendante** — 1=Mauvais, 2=Médiocre, 3=Bon, 4=Excellent |
| `calories_100g` | Quantitative | Calories pour 100g |
| `sucres_100g` | Quantitative | Sucres pour 100g |
| `graisses_saturees_100g` | Quantitative | Graisses saturées pour 100g |
| `sel_100g` | Quantitative | Sel pour 100g |
| `fibres_100g` | Quantitative | Fibres pour 100g |
| `proteines_100g` | Quantitative | Protéines pour 100g |
| `nb_additifs` | Quantitative | Nombre d'additifs |
| `bio` | Binaire (0/1) | Produit biologique |
| `ultra_transforme` | Binaire (0/1) | Produit ultra-transformé (classification NOVA) |
 
---
 
## Structure du projet
 
```
jeu_donnees_YUKA/
│
├── README.md
│
├── data/
│   └── jeu_donnees_yuka.csv
│
├── scripts/
│   ├── partie1_Palla.py          ← Présentation, stats descriptives, analyse exploratoire
│   ├── partie2_Havar.py          ← Méthodologie et estimation du modèle
│   └── partie3_Mouhammad.py      ← Évaluation, interprétation, choix du modèle
│
├── figures/                      ← Graphiques générés automatiquement
│
└── presentation/
    └── slides_yuka.pptx
```
 
---
 
## Répartition du travail
 
| Membre | Script | Contenu |
|---|---|---|
| Palla Gueye | `partie1_Palla.py` | Présentation des données · Statistiques descriptives · Analyse exploratoire |
| Havar Baskara | `partie2_Havar.py` | Méthodologie économétrique · Spécification · Estimation du Logit Ordonné |
| Mouhammad Gaye | `partie3_Mouhammad.py` | Évaluation des modèles · Interprétation · Choix du modèle final |
 
---
 
## Modèle économétrique retenu
 
La variable dépendante `score_yuka_ordonne` est **ordonnée** (4 catégories avec un ordre logique).
Ce caractère ordinal exclut la régression linéaire (Y n'est pas continue) et le logit binaire (plus de 2 catégories).
 
Le modèle retenu est le **Logit Ordonné** (*Ordered Logit*), qui modélise la probabilité
de passer d'une catégorie à la suivante en fonction des variables explicatives.
 
---
 
## Prérequis
 
```bash
pip install pandas numpy matplotlib seaborn scipy statsmodels
```
 
---
 
## Exécution
 
Lancer les scripts depuis le dossier `scripts/` :
 
```bash
cd scripts
python partie1_Palla.py
python partie2_Havar.py
python partie3_Mouhammad.py
```
 
Les figures sont automatiquement sauvegardées dans `figures/`.
 
---
 
## Principaux résultats (Partie 1)
 
- Sucres, sel, graisses saturées et nb_additifs : **effet négatif** attendu sur le score.
- Fibres et protéines : **effet positif** attendu.
- Produits bio : proportion d'Excellents nettement plus élevée (30.8% contre 13.6% chez les Mauvais).
- Produits ultra-transformés : 53.5% classés Mauvais, seulement 5.2% Excellents.
- Aucune multicolinéarité forte détectée (seuil conservateur 0.5).
- Toutes les variables significatives aux tests ANOVA et Chi² (p < 0.05).
---
 
## Modèle économétrique retenu

La variable dépendante `score_yuka_ordonne` est ordonnée (1 = Mauvais, 2 = Médiocre, 3 = Bon, 4 = Excellent).  
Ce caractère ordinal exclut la régression linéaire (variable non continue) ainsi que le logit binaire (plus de deux catégories).

Le modèle retenu est donc le **Logit Ordonné (Ordered Logit)**, qui permet de modéliser la probabilité d’appartenir à une catégorie en fonction des variables explicatives.

---

## Spécification du modèle

Les variables explicatives utilisées sont :

- calories_100g  
- sucres_100g  
- graisses_saturees_100g  
- sel_100g  
- fibres_100g  
- proteines_100g  
- nb_additifs  
- bio  
- ultra_transforme  

Le modèle est estimé sous Python avec la bibliothèque `statsmodels`.

## Modèle économétrique retenu

La variable dépendante `score_yuka_ordonne` est ordonnée (1 = Mauvais, 2 = Médiocre, 3 = Bon, 4 = Excellent).  
Ce caractère ordinal exclut la régression linéaire (variable non continue) ainsi que le logit binaire (plus de deux catégories).

Le modèle retenu est donc le **Logit Ordonné (Ordered Logit)**, qui permet de modéliser la probabilité d’appartenir à une catégorie en fonction des variables explicatives.

---

## Spécification du modèle

Les variables explicatives utilisées sont :

- calories_100g  
- sucres_100g  
- graisses_saturees_100g  
- sel_100g  
- fibres_100g  
- proteines_100g  
- nb_additifs  
- bio  
- ultra_transforme  

Le modèle est estimé sous Python avec la bibliothèque `statsmodels`.

## Modèle économétrique retenu

La variable dépendante `score_yuka_ordonne` est ordonnée (1 = Mauvais, 2 = Médiocre, 3 = Bon, 4 = Excellent).  
Ce caractère ordinal exclut la régression linéaire (variable non continue) ainsi que le logit binaire (plus de deux catégories).

Le modèle retenu est donc le **Logit Ordonné (Ordered Logit)**, qui permet de modéliser la probabilité d’appartenir à une catégorie en fonction des variables explicatives.

---

## Spécification du modèle

Les variables explicatives utilisées sont :

- calories_100g  
- sucres_100g  
- graisses_saturees_100g  
- sel_100g  
- fibres_100g  
- proteines_100g  
- nb_additifs  
- bio  
- ultra_transforme  

Le modèle est estimé sous Python avec la bibliothèque `statsmodels`.

---

## Résultats (Partie 2)

- Sucres, sel, graisses saturées et nombre d’additifs : effet négatif sur le score  
- Fibres et protéines : effet positif  
- Produits bio : probabilité plus élevée d’obtenir une bonne note  
- Produits ultra-transformés : forte probabilité d’avoir une mauvaise note  
- Toutes les variables sont statistiquement significatives (p < 0.05)

---

## Résultats détaillés

Les résultats complets du modèle sont disponibles dans le fichier `resultats_havar.txt`.

## Livrables
 
Conformément aux consignes de la prof :
 
- **Partie 1 (Yuka)** : script Python + présentation orale avec support visuel — soutenance le 7 mai 2026
- **Partie 2 (CDP)** : script Python + rapport écrit — deadline 4 mai 2026 à 23h59
---
 
*Cours dispensé par Mme Imen Ghattassi — Université Sorbonne Paris Nord*


