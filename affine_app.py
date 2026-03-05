import streamlit as st
import pandas as pd
import math

st.set_page_config(page_title="Codage Affine - Analyse Pédagogique", layout="wide")

st.title("📊 Structure du Cryptage Affine")
st.write("Visualisation de $f(x) = ax + b$ selon le quotient et le reste de la division par 26.")

# --- Paramètres ---
st.sidebar.header("Réglages")
a = st.sidebar.number_input("Coefficient a (multiplicateur)", value=3, step=1)
b = st.sidebar.number_input("Coefficient b (décalage)", value=2, step=1)

# Analyse mathématique
pgcd = math.gcd(a, 26)
if pgcd != 1:
    st.sidebar.error(f"⚠️ PGCD({a}, 26) = {pgcd}. Attention : des collisions vont apparaître (plusieurs lettres au même endroit).")
else:
    st.sidebar.success(f"✅ PGCD({a}, 26) = 1. Le codage est une permutation parfaite.")

# --- Préparation des données ---
alphabet = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")

# Calcul du quotient maximum pour définir le nombre de lignes
max_q = (a * 25 + b) // 26
lignes_quotient = range(max_q + 1)

# Création du dictionnaire pour le tableau
# La première ligne est l'alphabet de référence (les restes de 0 à 25)
tableau_data = {"Position (Reste)": [i for i in range(26)]}
tableau_data["Alphabet (Reste)"] = alphabet

# Initialisation des lignes de quotients
for q in lignes_quotient:
    tableau_data[f"Quotient q = {q}"] = [""] * 26

# Remplissage : on place la lettre d'origine x dans la case (q, r)
for x in range(26):
    y = a * x + b
    q = y // 26
    r = y % 26
    
    # Si la case est déjà occupée (cas pgcd != 1), on concatène pour montrer la collision
    if tableau_data[f"Quotient q = {q}"][r] == "":
        tableau_data[f"Quotient q = {q}"][r] = alphabet[x]
    else:
        tableau_data[f"Quotient q = {q}"][r] += f", {alphabet[x]}"

# Conversion en DataFrame et pivotement pour avoir l'alphabet en ligne
df = pd.DataFrame(tableau_data).set_index("Position (Reste)").transpose()

# --- Affichage ---
st.subheader("Tableau de répartition")
st.write("Ce tableau montre quelle lettre d'origine arrive sur quel reste (colonne) après combien de 'tours' de 26 (ligne).")

# On utilise st.table pour un rendu fixe et propre pour les élèves
st.table(df)

# --- Rappel de la formule ---
st.info(f"**Formule appliquée :** $x \\xrightarrow{{f}} {a}x + {b} = 26q + r$")
