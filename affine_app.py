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

# --- Section 2 : Visualisation Mathématique (VERSION CORRIGÉE) ---
st.divider()
st.subheader("📊 Détail du calcul par lettre")

alphabet = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")

# 1. Préparation des données pour le tableau
donnees_calcul = []

for x in range(26):
    lettre_origine = alphabet[x]
    y = a * x + b
    q = y // 26
    r = y % 26
    lettre_codee = alphabet[r]
    
    donnees_calcul.append({
        "Lettre Départ": lettre_origine,
        "x (Rang)": x,
        "ax + b": y,
        "q (Quotient)": q,
        "r (Reste)": r,
        "Lettre Finale": lettre_codee
    })

# 2. Création du DataFrame et inversion (Transpose)
# On met "Lettre Départ" en index pour qu'elle devienne l'en-tête après la transposition
df_math = pd.DataFrame(donnees_calcul).set_index("Lettre Départ").transpose()

# 3. Affichage
st.table(df_math)

st.info(f"""
**Comment lire ce tableau :**
* La première ligne est votre **alphabet source**.
* **ax + b** est la valeur brute avant le modulo.
* **q (Quotient)** indique combien de "tours" d'alphabet ont été faits (26, 52, etc.).
* **r (Reste)** est la position finale, qui donne la **Lettre Finale**.
""")

st.info(f"**Rappel Mathématique :** Chaque lettre de l'alphabet (ligne 1) est remplacée par la lettre située dans sa colonne. La ligne indique combien de fois on a 'bouclé' sur l'alphabet (le quotient de la division par 26).")
# --- Rappel de la formule ---
st.info(f"**Formule appliquée :** $x \\xrightarrow{{f}} {a}x + {b} = 26q + r$")
# --- Exemple détaillé avec la lettre M ---
st.subheader("🔍 Exemple de calcul détaillé")

# On définit la lettre exemple
lettre_test = "L"
x_test = ord(lettre_test) - ord('A')  # Rang de L (11)
y_test = a * x_test + b
q_test = y_test // 26
r_test = y_test % 26
lettre_codee = chr(r_test + ord('A'))

st.write(f"Prenons la lettre **{lettre_test}** :")

# Utilisation de colonnes pour une présentation "tableau noir"
c1, c2, c3 = st.columns(3)

with c1:
    st.markdown(f"1. Rang de la lettre :  \n$x = {x_test}$  \n(A=0, B=1, ..., L=11)")

with c2:
    st.markdown(f"2. Transformation :  \n$y = {a} \\times {x_test} + {b}$  \n$y = {y_test}$")

with c3:
    st.markdown(f"3. Division par 26 :  \n${y_test} = 26 \\times \\mathbf{{{q_test}}} + \\mathbf{{{r_test}}}$  \nLe reste est **{r_test}**")

st.success(f"👉 La lettre **{lettre_test}** (rang {x_test}) devient la lettre **{lettre_codee}** (rang {r_test}).")
