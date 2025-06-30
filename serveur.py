from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
import sqlite3
import os
from datetime import datetime
import requests

app = FastAPI()
templates = Jinja2Templates(directory="templates")
DB_PATH = "crm_ecommerce.db"
OLLAMA_URL = "http://localhost:11434/api/generate"

# Middleware (optionnel pour sécurité)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

def init_db():
    create = not os.path.exists(DB_PATH)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.executescript("""
    CREATE TABLE IF NOT EXISTS client (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT UNIQUE,
        nom TEXT,
        prenom TEXT
    );
    CREATE TABLE IF NOT EXISTS commande (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT,
        montant REAL,
        nb_articles INTEGER,
        id_client INTEGER,
        FOREIGN KEY(id_client) REFERENCES client(id)
    );
    """)
    if create:
        cursor.execute("INSERT INTO client (email, nom, prenom) VALUES (?, ?, ?)",
                       ("vendelin@iris.com", "Mille", "Vendelin"))
        cursor.execute("INSERT INTO commande (date, montant, nb_articles, id_client) VALUES (?, ?, ?, ?)",
                       (datetime.now().date().isoformat(), 0.0, 0, 1))
        conn.commit()
        print("[INIT] Base initialisée avec client de test.")
    conn.close()

def chercher_client_et_commande(email):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT * FROM client WHERE email=?", (email,))
    client = cur.fetchone()
    commande = None
    if client:
        cur.execute("SELECT * FROM commande WHERE id_client=? ORDER BY id DESC LIMIT 1", (client[0],))
        commande = cur.fetchone()
    conn.close()
    return client, commande

def generer_reponse_isabelle(email, message, client, commande):
    prenom = client[3] if client else email.split("@")[0].capitalize()
    if not commande:
        com_id = "nouvelle"
        base_info = "nous n'avons pas trouvé de commande associée à votre compte."
    else:
        com_id = commande[0]
        base_info = f"votre commande existe déjà (#{com_id})."

    prompt = f"""
Tu es Isabelle, secrétaire du service client de BKC (Blockchain + Burger King Company).

Bonjour {prenom},

Il semble que {base_info}
Le client souhaite passer commande. Voici son message :
\"\"\"{message}\"\"\"

Ta mission :
1. Catégorie : Produit
2. Rédige une réponse humaine et polie, en un seul paragraphe.
3. Informe que la commande #{com_id} est prise en charge,
   mais qu'il manque des détails : articles, quantités, mode de livraison.
4. Ne fais jamais de code, ne mentionne jamais la base de données.
5. N’utilise qu’un français naturel, cordial.
6. Signature avec « Isabelle - Service client BKC. »
"""

    try:
        resp = requests.post(OLLAMA_URL, json={
            "model": "adrienbrault/nous-hermes2pro:Q3_K_M",
            "prompt": prompt,
            "stream": False
        }, timeout=30)
        resp.raise_for_status()
        return resp.json().get("response", "[Réponse vide]").strip()
    except Exception as e:
        return f"[Erreur Ollama : {str(e)}]"

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/contact", response_class=HTMLResponse)
def handle_contact(request: Request, from_: str = Form(..., alias="from"), body: str = Form(...)):
    client, commande = chercher_client_et_commande(from_)
    reponse = generer_reponse_isabelle(from_, body, client, commande)
    return templates.TemplateResponse("index.html", {
        "request": request,
        "reponse": reponse
    })

# Initialisation de la base au démarrage
init_db()
