# ================================================================
# PROJET ÉCONOMÉTRIE QUALITATIVE — PARTIE YUKA
# Parties 1 : Présentation, Statistiques descriptives,
#                   Analyse exploratoire approfondie
# Master 1 BIDABI — Université Sorbonne Paris Nord
# ================================================================

# ── 0. IMPORTS ──────────────────────────────────────────────────
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import f_oneway, chi2_contingency

import warnings
warnings.filterwarnings("ignore")

# Chemins dynamiques (fonctionnent peu importe d'où on lance le script)
BASE_DIR    = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if not os.path.exists(os.path.join(BASE_DIR, "data")):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FIGURES_DIR = os.path.join(BASE_DIR, "figures")
os.makedirs(FIGURES_DIR, exist_ok=True)

# Style graphique cohérent
sns.set_theme(style="whitegrid", palette="Set2")
plt.rcParams["figure.dpi"] = 120

# ================================================================
# PARTIE 1 — PRÉSENTATION DES DONNÉES
# ================================================================

df = pd.read_csv(os.path.join(BASE_DIR, "data", "jeu_donnees_yuka.csv"),
                 sep=None, engine="python")
df = df.drop(columns=["id_produit"])

print("=" * 65)
print("PARTIE 1 — PRÉSENTATION DES DONNÉES")
print("=" * 65)

# ── 1.1 Dimensions ──────────────────────────────────────────────
print(f"\n📊 Nombre d'observations : {df.shape[0]}")
print(f"📊 Nombre de variables   : {df.shape[1]}")

# ── 1.2 Types des variables ──────────────────────────────────────
print("\n📋 Types des variables :")
print(df.dtypes)

print("""
🧠 Interprétation :
  - score_yuka_ordonne est notre variable dépendante ordonnée
    (1=Mauvais, 2=Médiocre, 3=Bon, 4=Excellent). Son caractère
    ordonné justifie l'usage d'un modèle Logit Ordonné plutôt
    qu'une régression linéaire ou un logit binaire.
  - Les variables quantitatives (calories, sucres, etc.) mesurent
    la composition nutritionnelle des produits.
  - Les variables qualitatives binaires (bio, ultra_transforme)
    capturent des caractéristiques structurelles du produit.
""")

# ── 1.3 Valeurs manquantes ───────────────────────────────────────
print("❓ Valeurs manquantes par variable :")
print(df.isnull().sum())
print("→ Aucune valeur manquante : le dataset est complet, aucun")
print("  traitement d'imputation n'est nécessaire.")

# ── 1.4 Distribution de la variable dépendante ──────────────────
print("\n📊 Distribution de score_yuka_ordonne (variable à expliquer) :")
dist_y = df["score_yuka_ordonne"].value_counts().sort_index()
labels = {1: "Mauvais", 2: "Médiocre", 3: "Bon", 4: "Excellent"}
for k, v in dist_y.items():
    print(f"  {k} — {labels[k]:10s} : {v:4d} produits ({100*v/len(df):.1f}%)")

print("""
🧠 Interprétation :
  La majorité des produits (36.8%) sont classés "Mauvais", ce qui
  reflète la réalité de l'offre alimentaire industrielle : beaucoup
  de produits transformés aux compositions nutritionnelles
  défavorables. Seulement 13.3% atteignent le score "Excellent".
  Cette distribution déséquilibrée est un fait stylisé important
  à mentionner avant l'estimation du modèle.
""")

# Graphique distribution Y
fig, ax = plt.subplots(figsize=(7, 4))
colors = ["#d32f2f", "#f57c00", "#388e3c", "#1565c0"]
bars = ax.bar([labels[k] for k in dist_y.index],
              dist_y.values, color=colors, edgecolor="white")
for bar, val in zip(bars, dist_y.values):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 5,
            f"{val}\n({100*val/len(df):.1f}%)",
            ha="center", va="bottom", fontsize=10)
ax.set_title("Distribution de la variable dépendante\nscore_yuka_ordonne",
             fontsize=13, fontweight="bold")
ax.set_ylabel("Nombre de produits")
ax.set_xlabel("Catégorie Yuka")
plt.tight_layout()
plt.savefig(os.path.join(FIGURES_DIR, "fig1_distribution_Y.png"))
plt.show()

# ================================================================
# PARTIE 2 — STATISTIQUES DESCRIPTIVES
# ================================================================

print("\n" + "=" * 65)
print("PARTIE 2 — STATISTIQUES DESCRIPTIVES")
print("=" * 65)

vars_quanti = ["calories_100g", "sucres_100g", "graisses_saturees_100g",
               "sel_100g", "fibres_100g", "proteines_100g", "nb_additifs"]
vars_quali  = ["bio", "ultra_transforme"]

# ── 2.1 Stats descriptives variables quantitatives ───────────────
print("\n📈 2.1 — Statistiques descriptives (variables quantitatives) :")
stats_desc = df[vars_quanti].agg(["mean", "std", "min",
                                   lambda x: x.quantile(0.25),
                                   "median",
                                   lambda x: x.quantile(0.75),
                                   "max"])
stats_desc.index = ["Moyenne", "Écart-type", "Min", "Q1", "Médiane", "Q3", "Max"]
print(stats_desc.round(3).to_string())

# Interprétation économique des stats descriptives
moy = df[vars_quanti].mean()
print(f"""
🧠 Interprétation économique :
  - Sucres : moyenne de {moy['sucres_100g']:.1f}g/100g. L'OMS recommande
    moins de 25g/jour d'ajoutés — un niveau moyen déjà préoccupant.
  - Sel : moyenne de {moy['sel_100g']:.2f}g/100g, cohérent avec une
    consommation industrielle souvent excessive en sodium.
  - Graisses saturées : {moy['graisses_saturees_100g']:.1f}g/100g en moyenne,
    associées aux risques cardiovasculaires.
  - Fibres : seulement {moy['fibres_100g']:.1f}g/100g en moyenne, bien en
    dessous des apports journaliers recommandés (25g/jour).
  - Additifs : en moyenne {moy['nb_additifs']:.1f} additifs par produit,
    indicateur clé de la transformation industrielle.
  → Ces niveaux suggèrent que les variables "néfastes" (sucres,
    sel, graisses, additifs) devraient avoir un effet négatif sur
    le score Yuka, et les variables "bénéfiques" (fibres, protéines)
    un effet positif.
""")

# ── 2.2 Histogrammes ────────────────────────────────────────────
fig, axes = plt.subplots(3, 3, figsize=(14, 10))
axes = axes.flatten()
for i, var in enumerate(vars_quanti):
    axes[i].hist(df[var], bins=30, color="#42a5f5", edgecolor="white", alpha=0.85)
    axes[i].set_title(var, fontsize=10, fontweight="bold")
    axes[i].set_ylabel("Fréquence")
for j in range(len(vars_quanti), len(axes)):
    axes[j].set_visible(False)
plt.suptitle("Distributions des variables quantitatives", fontsize=13, fontweight="bold")
plt.tight_layout()
plt.savefig(os.path.join(FIGURES_DIR, "fig2_histogrammes_quanti.png"))
plt.show()

# ── 2.3 Stats descriptives variables qualitatives ────────────────
print("\n📊 2.2 — Statistiques descriptives (variables qualitatives) :")
for var in vars_quali:
    freq = df[var].value_counts()
    print(f"\n  {var} :")
    print(f"    0 (Non) : {freq.get(0,0):4d} produits ({100*freq.get(0,0)/len(df):.1f}%)")
    print(f"    1 (Oui) : {freq.get(1,0):4d} produits ({100*freq.get(1,0)/len(df):.1f}%)")

print(f"""
🧠 Interprétation :
  - Bio : seulement 19.1% des produits sont biologiques. Le marché
    bio reste minoritaire mais en croissance — ces produits tendent
    à avoir moins d'additifs et de meilleurs profils nutritionnels.
  - Ultra-transformé : 36.6% des produits sont ultra-transformés
    (classification NOVA). Ce taux élevé reflète la structure de
    l'offre alimentaire moderne. Ces produits contiennent
    généralement plus d'additifs, de sucres et de graisses.
""")

# Barplots variables qualitatives
fig, axes = plt.subplots(1, 2, figsize=(10, 4))
for i, var in enumerate(vars_quali):
    freq = df[var].value_counts().sort_index()
    axes[i].bar(["Non (0)", "Oui (1)"], freq.values,
                color=["#ef9a9a", "#66bb6a"], edgecolor="white")
    for j, v in enumerate(freq.values):
        axes[i].text(j, v + 5, f"{v} ({100*v/len(df):.1f}%)",
                     ha="center", fontsize=10)
    axes[i].set_title(var, fontsize=11, fontweight="bold")
    axes[i].set_ylabel("Nombre de produits")
plt.suptitle("Distribution des variables qualitatives", fontsize=13, fontweight="bold")
plt.tight_layout()
plt.savefig(os.path.join(FIGURES_DIR, "fig3_barplots_quali.png"))
plt.show()

# ── 2.4 Matrice de corrélation ───────────────────────────────────
print("\n🔗 2.3 — Matrice de corrélation (variables quantitatives) :")
corr_matrix = df[vars_quanti].corr()
print(corr_matrix.round(3).to_string())

# Détecter les corrélations fortes
print("\n🧠 Analyse de la multicolinéarité :")
# Seuil conservateur de 0.5 (plus strict que le 0.7/0.8 souvent
# utilisé en économétrie — toute corrélation modérée est signalée)
seuil = 0.5
paires_fortes = []
for i in range(len(vars_quanti)):
    for j in range(i+1, len(vars_quanti)):
        r = corr_matrix.iloc[i, j]
        if abs(r) > seuil:
            paires_fortes.append((vars_quanti[i], vars_quanti[j], r))

if paires_fortes:
    print(f"  Corrélations > {seuil} (risque de multicolinéarité) :")
    for v1, v2, r in paires_fortes:
        print(f"    {v1} — {v2} : r = {r:.3f}")
    print("  → Ces variables partagent de l'information commune.")
    print("    Il faudra vérifier leur pertinence individuelle dans le modèle.")
else:
    print(f"  Aucune corrélation > {seuil} détectée entre les variables.")
    print("  → Aucune corrélation élevée détectée (seuil conservateur 0.5).")
    print("    On ne soupçonne pas de multicolinéarité forte, à confirmer")
    print("    lors de l'estimation du modèle.")
    print("    Toutes les variables peuvent être incluses en première approche.")

fig, ax = plt.subplots(figsize=(9, 7))
mask = np.triu(np.ones_like(corr_matrix, dtype=bool))
sns.heatmap(corr_matrix, mask=mask, annot=True, fmt=".2f",
            cmap="RdBu_r", center=0, vmin=-1, vmax=1,
            linewidths=0.5, ax=ax)
ax.set_title("Matrice de corrélation\n(variables quantitatives)",
             fontsize=13, fontweight="bold")
plt.tight_layout()
plt.savefig(os.path.join(FIGURES_DIR, "fig4_correlation.png"))
plt.show()

# ── 2.5 Tests de moyenne (ANOVA) ─────────────────────────────────
print("\n🔬 2.4 — Tests de moyenne (ANOVA) : X varie-t-elle selon le score Yuka ?")
print("  H0 : la moyenne de X est identique dans toutes les catégories de Y")
print("  H1 : au moins une catégorie a une moyenne différente")
print(f"\n  {'Variable':<30} {'F-stat':>10} {'p-value':>12} {'Significatif ?':>15}")
print("  " + "-" * 70)

groupes_y = [df[df["score_yuka_ordonne"] == k] for k in [1, 2, 3, 4]]
vars_sig_anova = []

for var in vars_quanti:
    groupes = [g[var].values for g in groupes_y]
    f_stat, p_val = f_oneway(*groupes)
    sig = "✅ OUI" if p_val < 0.05 else "❌ NON"
    if p_val < 0.05:
        vars_sig_anova.append(var)
    print(f"  {var:<30} {f_stat:>10.3f} {p_val:>12.4f} {sig:>15}")

print(f"""
🧠 Interprétation ANOVA :
  Pour chaque variable significative, on rejette H0 : la moyenne
  de X diffère selon la catégorie Yuka. Cela signifie que ces
  variables discriminent bien les produits selon leur score.
  → Variables retenues pour le modèle : {len(vars_sig_anova)}/{len(vars_quanti)}
  → {', '.join(vars_sig_anova)}
  → Toutes les variables quantitatives sont significatives au
    seuil de 5%, ce qui justifie leur inclusion dans le modèle
    Logit Ordonné.
  → Ces résultats suggèrent des différences de moyennes entre
    classes, sans préjuger de la forme fonctionnelle du modèle.
""")

# ── 2.6 Tests Chi² ───────────────────────────────────────────────
print("\n🔬 2.5 — Tests Chi² : X qualitative est-elle liée à Y ?")
print("  H0 : X et Y sont indépendantes")
print("  H1 : X et Y sont liées")
print(f"\n  {'Variable':<20} {'Chi2':>10} {'p-value':>12} {'Significatif ?':>15}")
print("  " + "-" * 60)

for var in vars_quali:
    table = pd.crosstab(df[var], df["score_yuka_ordonne"])
    chi2, p, dof, expected = chi2_contingency(table)
    sig = "✅ OUI" if p < 0.05 else "❌ NON"
    print(f"  {var:<20} {chi2:>10.3f} {p:>12.4f} {sig:>15}")

print("""
🧠 Interprétation Chi² :
  On rejette H0 pour bio et ultra_transforme : ces deux variables
  qualitatives sont significativement liées au score Yuka.
  → Un produit bio a tendance à obtenir un meilleur score.
  → Un produit ultra-transformé a tendance à obtenir un moins
    bon score — ce qui est économiquement cohérent avec la
    littérature sur la qualité nutritionnelle des aliments.
  → Les deux variables seront donc incluses dans le modèle.
""")

# Tableaux croisés
print("  Tableaux croisés (fréquences en %) :")
for var in vars_quali:
    table = pd.crosstab(df[var], df["score_yuka_ordonne"],
                        rownames=[var], colnames=["Score Yuka"],
                        normalize="index") * 100
    table.index = ["Non (0)", "Oui (1)"]
    table.columns = ["Mauvais", "Médiocre", "Bon", "Excellent"]
    print(f"\n  {var} :")
    print(table.round(1).to_string())

# ================================================================
# PARTIE 3 — ANALYSE EXPLORATOIRE APPROFONDIE
# ================================================================

print("\n" + "=" * 65)
print("PARTIE 3 — ANALYSE EXPLORATOIRE APPROFONDIE")
print("=" * 65)

# ── 3.1 Boxplots X par catégorie Y ──────────────────────────────
fig, axes = plt.subplots(3, 3, figsize=(14, 10))
axes = axes.flatten()
colors_box = ["#d32f2f", "#f57c00", "#388e3c", "#1565c0"]

for i, var in enumerate(vars_quanti):
    sns.boxplot(data=df, x="score_yuka_ordonne", y=var,
                palette=colors_box, ax=axes[i])
    axes[i].set_title(var, fontsize=10, fontweight="bold")
    axes[i].set_xlabel("Score Yuka (1=Mauvais → 4=Excellent)")
    axes[i].set_ylabel("")
    axes[i].set_xticklabels(["Mauvais", "Médiocre", "Bon", "Excellent"], fontsize=8)

for j in range(len(vars_quanti), len(axes)):
    axes[j].set_visible(False)

plt.suptitle("Boxplots : variables quantitatives par catégorie Yuka",
             fontsize=13, fontweight="bold")
plt.tight_layout()
plt.savefig(os.path.join(FIGURES_DIR, "fig5_boxplots_par_categorie.png"))
plt.show()

# ── 3.2 Moyennes par catégorie ───────────────────────────────────
print("\n📊 3.1 — Moyennes par catégorie Yuka :")
moyennes = df.groupby("score_yuka_ordonne")[vars_quanti].mean()
moyennes.index = ["Mauvais", "Médiocre", "Bon", "Excellent"]
print(moyennes.round(3).to_string())

# Interprétation détaillée par variable
print("\n🧠 Lecture économique des tendances :")
for var in vars_quanti:
    vals = moyennes[var].values
    tendance = "↘ décroissante" if vals[-1] < vals[0] else "↗ croissante"
    if var in ["fibres_100g", "proteines_100g"]:
        effet = "effet POSITIF attendu sur le score Yuka"
    elif var in ["sucres_100g", "sel_100g", "graisses_saturees_100g",
                 "nb_additifs", "calories_100g"]:
        effet = "effet NÉGATIF attendu sur le score Yuka"
    else:
        effet = "effet incertain"
    print(f"  {var:<30} tendance {tendance} → {effet}")

print("""
  Interprétation :
  - Les produits classés "Mauvais" ont en moyenne plus de sucres,
    sel, graisses saturées et additifs. Ces ingrédients sont
    reconnus comme facteurs de risque pour la santé, ce qui est
    cohérent avec la logique de notation Yuka.
  - Les produits "Excellent" ont plus de fibres et de protéines,
    associés à une meilleure qualité nutritionnelle.
  - Cette analyse exploratoire confirme nos hypothèses économiques
    et valide l'inclusion de toutes les variables dans le modèle.
""")

# ── 3.3 Variables quali par catégorie ───────────────────────────
print("\n📊 3.2 — Proportion bio et ultra-transformé par catégorie :")
for var in vars_quali:
    prop = df.groupby("score_yuka_ordonne")[var].mean() * 100
    prop.index = ["Mauvais", "Médiocre", "Bon", "Excellent"]
    print(f"\n  {var} (% de produits = 1) :")
    for cat, val in prop.items():
        print(f"    {cat:12s} : {val:.1f}%")

print("""
🧠 Interprétation :
  - bio : la proportion de produits bio augmente clairement avec
    le score Yuka (de ~13.6% chez les Mauvais à ~30.8% chez les
    Excellents). Être bio est associé à de meilleures pratiques
    de production, moins d'additifs et moins d'intrants chimiques.
  - ultra_transforme : la proportion chute fortement du bas vers
    le haut de l'échelle (~54% de Mauvais sont ultra-transformés
    contre seulement ~5% d'Excellents). Ce résultat est
    économiquement logique : la transformation industrielle
    intensive dégrade la qualité nutritionnelle.
""")

# Graphiques proportions
fig, axes = plt.subplots(1, 2, figsize=(12, 5))
for i, var in enumerate(vars_quali):
    prop = df.groupby("score_yuka_ordonne")[var].mean() * 100
    axes[i].bar(["Mauvais", "Médiocre", "Bon", "Excellent"],
                prop.values,
                color=["#d32f2f", "#f57c00", "#388e3c", "#1565c0"],
                edgecolor="white")
    for j, v in enumerate(prop.values):
        axes[i].text(j, v + 0.5, f"{v:.1f}%", ha="center", fontsize=10)
    axes[i].set_title(f"Proportion '{var}' par catégorie Yuka",
                      fontsize=11, fontweight="bold")
    axes[i].set_ylabel("% de produits")
    axes[i].set_xlabel("Catégorie Yuka")
plt.tight_layout()
plt.savefig(os.path.join(FIGURES_DIR, "fig6_quali_par_categorie.png"))
plt.show()

# ── 3.4 Synthèse et hypothèses économiques ──────────────────────
print("\n" + "=" * 65)
print("SYNTHÈSE — HYPOTHÈSES ÉCONOMIQUES ET VARIABLES RETENUES")
print("=" * 65)
print("""
Les statistiques descriptives et l'analyse exploratoire nous
permettent d'identifier les variables pertinentes avant
l'estimation économétrique.

Variables à effet NÉGATIF attendu sur le score Yuka :
  - sucres_100g       : plus de sucre → score plus bas
  - sel_100g          : plus de sel → score plus bas
  - graisses_saturees_100g : associées aux maladies cardio.
  - nb_additifs       : marqueur de transformation industrielle
  - calories_100g     : effet ambigu ou faible (significatif
    statistiquement mais tendance peu claire économiquement)
  - ultra_transforme  : score Yuka systématiquement dégradé

Variables à effet POSITIF attendu sur le score Yuka :
  - fibres_100g       : associées à une bonne qualité nutritive
  - proteines_100g    : facteur de qualité alimentaire
  - bio               : moins d'intrants, meilleur profil

Aucune corrélation élevée détectée… on ne soupçonne pas de 
multicolinéarité forte entre les variables explicatives 
(aucune corrélation > 0.5).

→ Toutes les variables sont retenues pour l'estimation du
  modèle Logit Ordonné (Parties 4, 5, 6).

Limite à garder en tête :
  Les résultats restent descriptifs et peuvent être influencés
  par des variables omises (ex : catégorie de produit, marque,
  prix). L'estimation économétrique permettra de contrôler
  ces effets partiellement.

Phrase clé :
"Les statistiques descriptives nous permettent d'identifier
les variables pertinentes avant l'estimation économétrique.
Cette analyse exploratoire permet d'éviter un modèle mal
spécifié. L'ensemble des variables présente une relation
significative avec le score Yuka, ce qui justifie leur
inclusion dans le modèle Logit Ordonné."
""")

print("✅ Script Parties 1, 2, 3 terminé.")
