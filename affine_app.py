import streamlit as st
import pandas as pd
import math
import unicodedata
import re

st.set_page_config(page_title="Codage Affine Pro", layout="wide")

st.title("🔐 Cryptage Affine Interactif")

# --- Fonctions de traitement de texte ---
def nettoyer_texte(texte):
    # 1. Passage en majuscules
    texte = texte.upper()
    # 2. Suppression des accents (Normalisation NFKD)
    texte = "".join(c for c in unicodedata.normalize('NFD', texte) if unicodedata.category(c) != 'Mn')
    # 3. Remplacer tout ce qui n'est pas A-Z par un espace
    texte = re.sub(r'[^A-Z]', ' ', texte)
    return texte

def crypter_affine(texte, a, b):
    resultat = ""
    for lettre in texte:
        if lettre == " ":
            resultat += " "
        else:
            x = ord(lettre) - ord('A')
            r = (a * x + b) % 26
            resultat += chr(r + ord('A'))
    return resultat

# --- Barre latérale : Paramètres ---
st.sidebar.header("⚙️ Paramètres de la clé")
a = st.sidebar.number_input("Coefficient a", value=3, step=1)
b = st.sidebar.number_input("Coefficient b (Décalage)", value=2, step=1)

pgcd = math.gcd(a, 26)
if pgcd != 1:
    st.sidebar.error(f"⚠️ PGCD({a}, 26) = {pgcd}. Le codage n'est pas réversible !")
else:
    st.sidebar.success("✅ Clé valide (Bijection)")

# --- Section 1 : Cryptage de message ---
st.subheader("📝 Tester un message")
message_u = st.text_area("Entrez le texte à crypter :", "Le codage affine, c'est génial !")

if message_u:
    message_propre = nettoyer_texte(message_u)
    message_code = crypter_affine(message_propre, a, b)
    
    col1, col2 = st.columns(2)
    with col1:
        st.caption("Texte prétraité (sans accents / spécial)")
        st.code(message_propre)
    with col2:
        st.caption("Texte crypté")
        st.code(message_code)

# --- Section 2 : Visualisation Mathématique ---
st.divider()
st.subheader("📊 Structure du Codage (Quotients et Restes)")

alphabet = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
max_q = (a * 25 + b) // 26
lignes_quotient = range(max_q + 1)

tableau_data = {"Position (Reste)": [i for i in range(26)]}
tableau_data["Alphabet cible"] = alphabet

for q in lignes_quotient:
    tableau_data[f"Quotient q = {q}"] = [""] * 26

for x in range(26):
    y = a * x + b
    q = y // 26
    r = y % 26
    cell_content = alphabet[x]
    if tableau_data[f"Quotient q = {q}"][r] == "":
        tableau_data[f"Quotient q = {q}"][r] = cell_content
    else:
        tableau_data[f"Quotient q = {q}"][r] += f", {cell_content}"

df = pd.DataFrame(tableau_data).set_index("Position (Reste)").transpose()
st.table(df)

st.info(f"**Rappel Mathématique :** Chaque lettre de l'alphabet (ligne 1) est remplacée par la lettre située dans sa colonne. La ligne indique combien de fois on a 'bouclé' sur l'alphabet (le quotient de la division par 26).")
# --- Rappel de la formule ---
st.info(f"**Formule appliquée :** $x \\xrightarrow{{f}} {a}x + {b} = 26q + r$")
# --- Exemple détaillé avec la lettre M ---
st.subheader("🔍 Exemple de calcul détaillé")

# On définit la lettre exemple
lettre_test = "M"
x_test = ord(lettre_test) - ord('A')  # Rang de M (12)
y_test = a * x_test + b
q_test = y_test // 26
r_test = y_test % 26
lettre_codee = chr(r_test + ord('A'))

st.write(f"Prenons la lettre **{lettre_test}** :")

# Utilisation de colonnes pour une présentation "tableau noir"
c1, c2, c3 = st.columns(3)

with c1:
    st.markdown(f"**1. Rang de la lettre** \n$x = {x_test}$  \n(A=0, B=1, ..., M=12)")

with c2:
    st.markdown(f"**2. Transformation** \n$y = {a} \\times {x_test} + {b}$  \n$y = {y_test}$")

with c3:
    st.markdown(f"**3. Division par 26** \n${y_test} = 26 \\times \\mathbf{{{q_test}}} + \\mathbf{{{r_test}}}$  \nLe reste est **{r_test}**")

st.success(f"👉 La lettre **{lettre_test}** (rang {x_test}) devient la lettre **{lettre_codee}** (rang {r_test}).")
