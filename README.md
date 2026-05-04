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

La variable dépendante `score_yuka_ordonne` est une variable **ordonnée** (1 = Mauvais, 2 = Médiocre, 3 = Bon, 4 = Excellent).

Ce caractère ordinal exclut l’utilisation :

* d’une régression linéaire (variable non continue)
* d’un logit binaire (plus de deux catégories)

Le modèle retenu est donc un **logit ordonné (Ordered Logit)**, qui permet de modéliser la probabilité d’appartenir à une catégorie de score en fonction des variables explicatives.

Trois spécifications ont été estimées :

* **Modèle 1 : Complet (saturé)**
  Inclut toutes les variables explicatives :
  `graisses_saturees_100g`, `sel_100g`, `fibres_100g`, `proteines_100g`, `nb_additifs`, `bio`, `ultra_transforme`

* **Modèle 2 : Nutrition seule**
  Inclut uniquement les variables nutritionnelles :
  `graisses_saturees_100g`, `sel_100g`, `fibres_100g`, `proteines_100g`

* **Modèle 3 : Sans ultra_transformé**
  Permet d’évaluer l’impact spécifique de la variable `ultra_transforme`

La comparaison des modèles repose sur les critères AIC et BIC.

Le **Modèle 1 (complet)** présente les meilleures performances (AIC et BIC les plus faibles).
Il est donc retenu comme modèle final.

---

## Spécification du modèle retenu

Les variables explicatives du modèle final sont :

* graisses_saturees_100g
* sel_100g
* fibres_100g
* proteines_100g
* nb_additifs
* bio
* ultra_transforme

Le modèle est estimé sous Python à l’aide de la bibliothèque `statsmodels`.

---

## Résultats (Partie 2)

Les résultats obtenus montrent que :

* Les **graisses saturées**, le **sel** et le **nombre d’additifs** ont un **effet négatif significatif** sur la note Yuka
* Les **fibres** et les **protéines** ont un **effet positif significatif**
* Les produits **bio** ont une probabilité plus élevée d’obtenir une bonne note
* Les produits **ultra-transformés** ont une forte probabilité d’obtenir une mauvaise note

Toutes les variables sont statistiquement significatives (p < 0.05).

---

## Résultats détaillés

Les résultats complets des estimations sont disponibles dans le fichier :

`results_havar.txt`

---


## Livrables
 
Conformément aux consignes de la prof :
 
- **Partie 1 (Yuka)** : script Python + présentation orale avec support visuel — soutenance le 7 mai 2026
- **Partie 2 (CDP)** : script Python + rapport écrit — deadline 4 mai 2026 à 23h59
---
 
*Cours dispensé par Mme Imen Ghattassi — Université Sorbonne Paris Nord*


