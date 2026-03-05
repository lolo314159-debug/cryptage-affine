import streamlit as st
import pandas as pd
import numpy as np
import math

st.set_page_config(page_title="Visualisation Codage Affine", layout="wide")

st.title("🧪 Visualisation du Cryptage Affine")
st.write("Analyse de la transformation $f(x) = ax + b$")

# --- Barre latérale pour les paramètres ---
st.sidebar.header("Paramètres de codage")
a = st.sidebar.number_input("Coefficient a", value=3, step=1)
b = st.sidebar.number_input("Coefficient b (Décalage)", value=2, step=1)

# Vérification mathématique du PGCD
pgcd_a_26 = math.gcd(a, 26)
if pgcd_a_26 != 1:
    st.sidebar.error(f"⚠️ pgcd({a}, 26) = {pgcd_a_26}. Le codage ne sera pas bijectif (plusieurs lettres auront le même code).")
else:
    st.sidebar.success(f"✅ pgcd({a}, 26) = 1. Le codage est valide.")

# --- Calculs ---
alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
data = []

# On calcule pour chaque lettre son image, son quotient et son reste
for x in range(26):
    y = a * x + b
    q = y // 26
    r = y % 26
    data.append({
        "Original": alphabet[x],
        "x": x,
        "f(x)": y,
        "Quotient (q)": q,
        "Reste (r)": r,
        "Codé": alphabet[r]
    })

df_calc = pd.DataFrame(data)

# --- Construction du tableau visuel ---
# On détermine le quotient max pour définir le nombre de lignes
max_q = df_calc["Quotient (q)"].max()

# Création d'une matrice vide remplie d'espaces
# Colonnes de 0 à 25, Lignes de 0 à max_q
grid = np.full((max_q + 1, 26), "", dtype=object)

# Remplissage de la grille
# La ligne 0 contient l'alphabet original (en option, ou on commence à la ligne des restes)
for _, row in df_calc.iterrows():
    grid[row["Quotient (q)"], row["Reste (r)"]] = f"{row['Original']}→{row['Codé']}"

df_grid = pd.DataFrame(grid, columns=[i for i in range(26)])

# --- Affichage ---
st.subheader("Structure du Codage")

# Ligne de référence : L'alphabet source
st.write("**Alphabet d'origine (position x) :**")
st.table(pd.DataFrame([list(alphabet)], columns=[i for i in range(26)]))

st.write("**Répartition par Quotient (lignes) et Reste (colonnes) :**")
st.write("Chaque cellule montre la lettre d'origine et sa transformation.")
st.dataframe(df_grid)

# --- Détails techniques ---
with st.expander("Voir le détail des calculs"):
    st.table(df_calc)
