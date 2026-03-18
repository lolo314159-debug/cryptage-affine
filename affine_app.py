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

# --- Section 2 : Visualisation Mathématique (Grille par Quotient) ---
st.divider()
st.subheader("📊 Répartition par Quotient et Reste")

alphabet = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")

# 1. Calcul des bornes du quotient pour créer les lignes
q_min = (a * 0 + b) // 26
q_max = (a * 25 + b) // 26
lignes_quotient = [f"Quotient q = {q}" for q in range(q_min, q_max + 1)]

# 2. Initialisation du tableau avec l'alphabet de base en ligne 1
# On crée un DataFrame vide avec 26 colonnes (0 à 25)
df_grille = pd.DataFrame("", index=["Alphabet (Reste)"] + lignes_quotient, columns=range(26))

# Remplissage de la ligne 1 : Alphabet de base (le "Reste" cible)
df_grille.iloc[0] = alphabet

# 3. Remplissage des cellules avec les lettres d'origine
for x in range(26):
    y = a * x + b
    q = y // 26
    r = y % 26
    lettre_origine = alphabet[x]
    
    label_ligne = f"Quotient q = {q}"
    
    # On ajoute la lettre dans la case correspondante
    # (Gestion du cas où plusieurs lettres tomberaient dans la même case si PGCD != 1)
    if df_grille.at[label_ligne, r] == "":
        df_grille.at[label_ligne, r] = lettre_origine
    else:
        df_grille.at[label_ligne, r] += f", {lettre_origine}"

# 4. Affichage
st.table(df_grille)

st.info(f"""
**Lecture du tableau :**
* La **Ligne 1** est l'alphabet de destination (le reste $r$ de la division par 26).
* Les **Lignes suivantes** affichent les lettres d'origine placées selon leur quotient $q$.
* **Exemple :** Si la lettre **A** est dans la colonne **C** sur la ligne **Quotient 0**, cela signifie que $f(A)$ donne un reste de 2 (C) avec un quotient de 0.
""")# --- Rappel de la formule ---
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
