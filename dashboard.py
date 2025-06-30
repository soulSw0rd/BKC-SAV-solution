import streamlit as st
import sqlite3
import pandas as pd

DB_PATH = "crm_ecommerce.db"

def get_conn():
    return sqlite3.connect(DB_PATH)

def load_df(table):
    conn = get_conn()
    df = pd.read_sql_query(f"SELECT * FROM {table}", conn)
    conn.close()
    return df

def save_df(table, df):
    conn = get_conn()
    df.to_sql(table, conn, if_exists="replace", index=False)
    conn.close()

def afficher_table(table):
    df = load_df(table)
    st.subheader(f"Table : {table}")
    st.dataframe(df)
    st.download_button(f"Télécharger {table}.csv", df.to_csv(index=False), file_name=f"{table}.csv", mime="text/csv")

# CRUD fonctions existantes pour client, commande, article

def ajouter_article_commande():
    with st.form("ajout_article"):
        st.subheader("Ajouter un article à une commande")
        id_commande = st.number_input("ID Commande", min_value=1)
        nom_article = st.text_input("Nom de l'article")
        quantite = st.number_input("Quantité", min_value=1)
        prix_unitaire = st.number_input("Prix unitaire (€)", min_value=0.0, format="%.2f")
        submitted = st.form_submit_button("Ajouter")
        if submitted:
            conn = get_conn()
            conn.execute("""INSERT INTO article_commande
                            (id_commande, nom_article, quantite, prix_unitaire)
                            VALUES (?, ?, ?, ?)""",
                         (id_commande, nom_article, quantite, prix_unitaire))
            conn.commit()
            conn.close()
            st.success("Article ajouté")

def supprimer_ligne(table, id_col):
    df = load_df(table)
    if id_col in df:
        selected = st.selectbox(f"ID à supprimer dans {table}", df[id_col].tolist())
        if st.button(f"Supprimer ID {selected}"):
            conn = get_conn()
            conn.execute(f"DELETE FROM {table} WHERE {id_col} = ?", (selected,))
            conn.commit()
            conn.close()
            st.success("Supprimé")
            st.experimental_rerun()

def calcul_montant_commandes():
    conn = get_conn()
    df = pd.read_sql_query("""
    SELECT c.id AS id_commande,
           SUM(ac.quantite * ac.prix_unitaire) AS montant_calcule
    FROM commande c
    LEFT JOIN article_commande ac ON ac.id_commande = c.id
    GROUP BY c.id
    """, conn)
    conn.close()
    st.subheader("📊 Montant calculé par commande")
    st.dataframe(df)
    st.download_button("Télécharger montants.csv", df.to_csv(index=False), file_name="montants.csv")

def produit_plus_vendu():
    conn = get_conn()
    df = pd.read_sql_query("""
    SELECT nom_article, SUM(quantite) AS total_vendu
    FROM article_commande
    GROUP BY nom_article
    ORDER BY total_vendu DESC
    """, conn)
    conn.close()
    st.subheader("📈 Produits les plus vendus")
    st.bar_chart(df.set_index('nom_article')['total_vendu'])
    st.download_button("Télécharger top_produits.csv", df.to_csv(index=False), file_name="top_produits.csv")

st.set_page_config(page_title="Dashboard BDD", layout="wide")
st.title("📊 Dashboard BDD BKC – Avancé")

menu = st.sidebar.selectbox("Menu", [
    "Clients", "Commandes", "Articles de commande", "Contacts",
    "Ajouter client", "Ajouter commande", "Ajouter article",
    "Suppression", "Montants", "Top produits"
])

if menu == "Clients":
    afficher_table("client")
elif menu == "Commandes":
    afficher_table("commande")
elif menu == "Contacts":
    afficher_table("contact_client")
elif menu == "Articles de commande":
    afficher_table("article_commande")
elif menu == "Ajouter client":
    # code d'ajout client...
    pass
elif menu == "Ajouter commande":
    # code d'ajout commande...
    pass
elif menu == "Ajouter article":
    ajouter_article_commande()
elif menu == "Suppression":
    supprimer_ligne("client", "id")
    supprimer_ligne("commande", "id")
    supprimer_ligne("article_commande", "id")
    supprimer_ligne("contact_client", "id")
elif menu == "Montants":
    calcul_montant_commandes()
elif menu == "Top produits":
    produit_plus_vendu()
