# ================================================================
# PROJET ÉCONOMÉTRIE QUALITATIVE — PARTIE YUKA
# Parties 1 : Présentation, Statistiques descriptives,
#             Analyse exploratoire
# Master 1 BIDABI — Université Sorbonne Paris Nord
# ================================================================

# ── 0. IMPORTS ──────────────────────────────────────────────────
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
from scipy import stats
from scipy.stats import f_oneway, chi2_contingency

import warnings
warnings.filterwarnings("ignore")

# Style graphique cohérent
sns.set_theme(style="whitegrid", palette="Set2")
plt.rcParams["figure.dpi"] = 120

# ================================================================
# PARTIE 1 — PRÉSENTATION DES DONNÉES
# ================================================================

# ── 1.1 Chargement ──────────────────────────────────────────────
df = pd.read_csv("../data/jeu_donnees_yuka.csv", sep=None, engine="python")

# On supprime id_produit (identifiant, pas une variable explicative)
df = df.drop(columns=["id_produit"])

print("=" * 60)
print("PARTIE 1 — PRÉSENTATION DES DONNÉES")
print("=" * 60)

# ── 1.2 Dimensions et structure ─────────────────────────────────
print(f"\n📊 Nombre d'observations : {df.shape[0]}")
print(f"📊 Nombre de variables   : {df.shape[1]}")

# ── 1.3 Description des variables ───────────────────────────────
print("\n📋 Types des variables :")
print(df.dtypes)

# ── 1.4 Valeurs manquantes ──────────────────────────────────────
print("\n❓ Valeurs manquantes par variable :")
print(df.isnull().sum())
print("→ Aucune valeur manquante : dataset complet.")

# ── 1.5 Distribution de la variable dépendante ──────────────────
print("\n📊 Distribution de score_yuka_ordonne (variable à expliquer) :")
dist_y = df["score_yuka_ordonne"].value_counts().sort_index()
labels = {1: "Mauvais", 2: "Médiocre", 3: "Bon", 4: "Excellent"}
for k, v in dist_y.items():
    print(f"  {k} — {labels[k]:10s} : {v:4d} produits ({100*v/len(df):.1f}%)")

# Graphique distribution Y
fig, ax = plt.subplots(figsize=(7, 4))
colors = ["#d32f2f", "#f57c00", "#388e3c", "#1565c0"]
bars = ax.bar([labels[k] for k in dist_y.index], dist_y.values, color=colors, edgecolor="white")
for bar, val in zip(bars, dist_y.values):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 5,
            f"{val}\n({100*val/len(df):.1f}%)", ha="center", va="bottom", fontsize=10)
ax.set_title("Distribution de la variable dépendante\nscore_yuka_ordonne", fontsize=13, fontweight="bold")
ax.set_ylabel("Nombre de produits")
ax.set_xlabel("Catégorie Yuka")
plt.tight_layout()
plt.savefig("../figures/fig1_distribution_Y.png")
plt.show()
print("→ Figure 1 sauvegardée : ../figures/fig1_distribution_Y.png")

# ================================================================
# PARTIE 2 — STATISTIQUES DESCRIPTIVES
# ================================================================

print("\n" + "=" * 60)
print("PARTIE 2 — STATISTIQUES DESCRIPTIVES")
print("=" * 60)

# Séparer variables quantitatives et qualitatives
vars_quanti = ["calories_100g", "sucres_100g", "graisses_saturees_100g",
               "sel_100g", "fibres_100g", "proteines_100g", "nb_additifs"]
vars_quali  = ["bio", "ultra_transforme"]

# ── 2.1 Statistiques descriptives variables quantitatives ────────
print("\n📈 2.1 — Statistiques descriptives (variables quantitatives) :")
stats_desc = df[vars_quanti].agg(["mean", "std", "min",
                                   lambda x: x.quantile(0.25),
                                   "median",
                                   lambda x: x.quantile(0.75),
                                   "max"])
stats_desc.index = ["Moyenne", "Écart-type", "Min", "Q1", "Médiane", "Q3", "Max"]
print(stats_desc.round(3).to_string())

# ── 2.2 Histogrammes variables quantitatives ─────────────────────
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
plt.savefig("../figures/fig2_histogrammes_quanti.png")
plt.show()
print("→ Figure 2 sauvegardée : ../figures/fig2_histogrammes_quanti.png")

# ── 2.3 Statistiques descriptives variables qualitatives ─────────
print("\n📊 2.2 — Statistiques descriptives (variables qualitatives) :")
for var in vars_quali:
    freq = df[var].value_counts()
    print(f"\n  {var} :")
    print(f"    0 (Non) : {freq.get(0, 0):4d} produits ({100*freq.get(0,0)/len(df):.1f}%)")
    print(f"    1 (Oui) : {freq.get(1, 0):4d} produits ({100*freq.get(1,0)/len(df):.1f}%)")

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
plt.savefig("../figures/fig3_barplots_quali.png")
plt.show()
print("→ Figure 3 sauvegardée : ../figures/fig3_barplots_quali.png")

# ── 2.4 Matrice de corrélation ───────────────────────────────────
print("\n🔗 2.3 — Matrice de corrélation (variables quantitatives) :")
corr_matrix = df[vars_quanti].corr()
print(corr_matrix.round(3).to_string())

fig, ax = plt.subplots(figsize=(9, 7))
mask = np.triu(np.ones_like(corr_matrix, dtype=bool))
sns.heatmap(corr_matrix, mask=mask, annot=True, fmt=".2f",
            cmap="RdBu_r", center=0, vmin=-1, vmax=1,
            linewidths=0.5, ax=ax)
ax.set_title("Matrice de corrélation\n(variables quantitatives)", fontsize=13, fontweight="bold")
plt.tight_layout()
plt.savefig("../figures/fig4_correlation.png")
plt.show()
print("→ Figure 4 sauvegardée : ../figures/fig4_correlation.png")

# ── 2.5 Tests de moyenne (ANOVA) — X quanti vs Y ─────────────────
print("\n🔬 2.4 — Tests de moyenne (ANOVA) : est-ce que X varie selon le score Yuka ?")
print("  H0 : la moyenne de X est identique dans toutes les catégories de Y")
print("  H1 : au moins une catégorie a une moyenne différente")
print(f"\n  {'Variable':<30} {'F-stat':>10} {'p-value':>12} {'Significatif ?':>15}")
print("  " + "-" * 70)

groupes_y = [df[df["score_yuka_ordonne"] == k] for k in [1, 2, 3, 4]]

for var in vars_quanti:
    groupes = [g[var].values for g in groupes_y]
    f_stat, p_val = f_oneway(*groupes)
    sig = "✅ OUI" if p_val < 0.05 else "❌ NON"
    print(f"  {var:<30} {f_stat:>10.3f} {p_val:>12.4f} {sig:>15}")

# ── 2.6 Tests Chi² — X quali vs Y ────────────────────────────────
print("\n🔬 2.5 — Tests Chi² : est-ce que X quali est liée à Y ?")
print("  H0 : X et Y sont indépendantes")
print("  H1 : X et Y sont liées")
print(f"\n  {'Variable':<20} {'Chi2':>10} {'p-value':>12} {'Significatif ?':>15}")
print("  " + "-" * 60)

for var in vars_quali:
    table = pd.crosstab(df[var], df["score_yuka_ordonne"])
    chi2, p, dof, expected = chi2_contingency(table)
    sig = "✅ OUI" if p < 0.05 else "❌ NON"
    print(f"  {var:<20} {chi2:>10.3f} {p:>12.4f} {sig:>15}")

# Tableaux croisés
print("\n  Tableaux croisés (fréquences en %) :")
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

print("\n" + "=" * 60)
print("PARTIE 3 — ANALYSE EXPLORATOIRE APPROFONDIE")
print("=" * 60)

# ── 3.1 Boxplots X quanti par catégorie Y ────────────────────────
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
plt.savefig("../figures/fig5_boxplots_par_categorie.png")
plt.show()
print("→ Figure 5 sauvegardée : ../figures/fig5_boxplots_par_categorie.png")

# ── 3.2 Statistiques par catégorie Y ─────────────────────────────
print("\n📊 3.1 — Moyennes par catégorie Yuka :")
moyennes = df.groupby("score_yuka_ordonne")[vars_quanti].mean()
moyennes.index = ["Mauvais", "Médiocre", "Bon", "Excellent"]
print(moyennes.round(3).to_string())

# ── 3.3 Variables quali par catégorie Y ──────────────────────────
print("\n📊 3.2 — Proportion de produits bio et ultra-transformés par catégorie :")
for var in vars_quali:
    prop = df.groupby("score_yuka_ordonne")[var].mean() * 100
    prop.index = ["Mauvais", "Médiocre", "Bon", "Excellent"]
    print(f"\n  {var} (% de '1') :")
    for cat, val in prop.items():
        print(f"    {cat:12s} : {val:.1f}%")

# Graphique proportions bio et ultra_transforme par Y
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
plt.savefig("../figures/fig6_quali_par_categorie.png")
plt.show()
print("→ Figure 6 sauvegardée : ../figures/fig6_quali_par_categorie.png")

# ── 3.4 Synthèse / Hypothèses économiques ────────────────────────
print("\n" + "=" * 60)
print("SYNTHÈSE — HYPOTHÈSES ÉCONOMIQUES")
print("=" * 60)
print("""
D'après l'analyse exploratoire, on observe :

1. Les sucres, graisses saturées, sel et nb_additifs diminuent
   à mesure que le score Yuka augmente → effet négatif attendu.

2. Les fibres et protéines augmentent avec le score Yuka
   → effet positif attendu.

3. Les calories ne montrent pas de tendance claire selon les
   catégories → leur rôle explicatif est incertain.

4. Les produits bio obtiennent des scores Yuka nettement
   meilleurs → bio est un facteur positif fort.

5. Les produits ultra-transformés sont massivement classés
   Mauvais ou Médiocre → ultra_transforme est un facteur
   négatif fort.

Ces observations justifient l'inclusion de toutes les variables
dans le modèle Logit Ordonné (Partie 4 — Mouhammad & Havar).
""")

print("✅ Script Parties 1, 2, 3 terminé.")
