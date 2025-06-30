# BKC-SAV-Solution

Système de Service Après Vente intelligent pour BKC (Blockchain + Burger King Company) avec assistante IA Isabelle et dashboard de gestion.

## Description

Ce projet combine une **interface de service client intelligente** et un **dashboard de gestion CRM** pour une entreprise e-commerce. L'assistante virtuelle **Isabelle** traite automatiquement les demandes clients en utilisant un modèle de langage local, tandis que le dashboard permet de gérer la base de données clients, commandes et articles.

## Fonctionnalités

### 🤖 Assistante IA Isabelle
- **Traitement automatique** des e-mails clients
- **Réponses contextuelles** basées sur l'historique client
- **Intégration avec Ollama** (modèle : `adrienbrault/nous-hermes2pro:Q3_K_M`)
- **Interface web moderne** avec formulaire de contact
- **Gestion des commandes** et suivi client

### 📊 Dashboard CRM
- **Visualisation des données** clients, commandes et articles
- **Gestion CRUD complète** (Create, Read, Update, Delete)
- **Calculs automatiques** de montants de commandes
- **Analyses statistiques** (produits les plus vendus)
- **Export de données** au format CSV
- **Interface Streamlit** moderne et interactive

## Architecture

```
BKC-SAV-solution/
├── serveur.py          # API FastAPI pour l'assistante Isabelle
├── dashboard.py        # Dashboard Streamlit pour la gestion CRM
├── templates/
│   └── index.html     # Interface web du service client
├── requirements.txt    # Dépendances Python
└── README.md          # Documentation
```

## Prérequis

### 1. Ollama et modèle LLM
Installez Ollama et téléchargez le modèle :
```bash
# Installation d'Ollama (voir https://ollama.ai)
ollama pull adrienbrault/nous-hermes2pro:Q3_K_M
```

### 2. Python 3.8+
Assurez-vous d'avoir Python 3.8 ou plus récent installé.

## Installation

1. **Clonez le repository :**
```bash
git clone <repository-url>
cd BKC-SAV-solution
```

2. **Installez les dépendances :**
```bash
pip install -r requirements.txt
```

3. **Démarrez Ollama :**
```bash
ollama serve
```

## Utilisation

### 🚀 Lancement du service client (Isabelle)

```bash
# Démarrer l'API FastAPI
uvicorn serveur:app --reload --host 0.0.0.0 --port 8000
```

Accédez à l'interface à : `http://localhost:8000`

**Fonctionnalités disponibles :**
- Envoi d'e-mails de demande de support
- Réponses automatiques personnalisées par Isabelle
- Recherche automatique dans la base clients
- Création/mise à jour de commandes

### 📊 Lancement du dashboard CRM

```bash
# Démarrer le dashboard Streamlit
streamlit run dashboard.py
```

Accédez au dashboard à : `http://localhost:8501`

**Fonctionnalités disponibles :**
- **Visualisation** : Clients, Commandes, Articles, Contacts
- **Ajout** : Nouveaux clients, commandes, articles
- **Suppression** : Gestion des données obsolètes
- **Analytics** : Montants par commande, top produits
- **Export** : Téléchargement CSV de toutes les données

## Base de données

Le système utilise **SQLite** avec les tables suivantes :

### Table `client`
```sql
id INTEGER PRIMARY KEY AUTOINCREMENT
email TEXT UNIQUE
nom TEXT
prenom TEXT
```

### Table `commande`
```sql
id INTEGER PRIMARY KEY AUTOINCREMENT
date TEXT
montant REAL
nb_articles INTEGER
id_client INTEGER (FOREIGN KEY)
```

### Table `article_commande`
```sql
id INTEGER PRIMARY KEY AUTOINCREMENT
id_commande INTEGER
nom_article TEXT
quantite INTEGER
prix_unitaire REAL
```

### Table `contact_client`
```sql
id INTEGER PRIMARY KEY AUTOINCREMENT
id_client INTEGER
date_contact TEXT
message TEXT
reponse TEXT
```

## Configuration

### Modèle LLM
Le modèle utilisé est configuré dans `serveur.py` :
```python
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "adrienbrault/nous-hermes2pro:Q3_K_M"
```

### Base de données
```python
DB_PATH = "crm_ecommerce.db"
```

## API Endpoints

### Service Client (FastAPI)
- `GET /` - Interface web du service client
- `POST /contact` - Traitement des demandes clients

### Dashboard (Streamlit)
Interface web complète accessible via le navigateur.

## Exemples d'utilisation

### 1. Simulation d'une demande client
```
From: client@example.com
Subject: Problème commande
Body: Bonjour, je souhaite passer une commande de 3 burgers et 2 frites. Merci !
```

**Réponse d'Isabelle :**
```
Bonjour Client,

Merci pour votre message. Votre commande #1 est bien prise en charge. 
Cependant, pour finaliser votre commande de burgers et frites, j'aurais 
besoin de quelques précisions : quel type de burgers souhaitez-vous, 
quelle taille pour les frites, et quel mode de livraison préférez-vous ?

Isabelle - Service client BKC.
```

### 2. Analyse des ventes
Le dashboard permet de :
- Voir les produits les plus vendus en temps réel
- Calculer automatiquement les montants de commandes
- Exporter les données pour des analyses externes

## Sécurité

- **CORS** configuré pour les environnements de développement
- **Validation** des entrées utilisateur
- **Gestion d'erreurs** robuste avec Ollama
- **Base de données** locale (SQLite)

## Développement

### Structure du code
- **`serveur.py`** : API FastAPI, logique métier, intégration Ollama
- **`dashboard.py`** : Interface Streamlit, visualisations, CRUD
- **`templates/index.html`** : Frontend service client (HTML/CSS/JS)

### Ajout de fonctionnalités
1. **Nouveaux endpoints** : Modifiez `serveur.py`
2. **Nouveaux graphiques** : Ajoutez dans `dashboard.py`
3. **Nouvelles tables** : Mettez à jour `init_db()` dans `serveur.py`

## Dépendances

- **FastAPI** (>=0.104.0) : Framework web API
- **Uvicorn** (>=0.24.0) : Serveur ASGI
- **Streamlit** (>=1.28.0) : Dashboard interactif
- **Requests** (>=2.31.0) : Communication avec Ollama
- **Pandas** (>=2.1.0) : Manipulation de données
- **Jinja2** (>=3.1.0) : Templates HTML
- **SQLite3** : Base de données (inclus avec Python)

## Déploiement

### Développement
```bash
# Terminal 1 : Service client
uvicorn serveur:app --reload

# Terminal 2 : Dashboard
streamlit run dashboard.py

# Terminal 3 : Ollama
ollama serve
```

### Production
```bash
# Service client (production)
uvicorn serveur:app --host 0.0.0.0 --port 8000

# Dashboard (production)
streamlit run dashboard.py --server.port 8501 --server.address 0.0.0.0
```

## Troubleshooting

### Problèmes courants

1. **Ollama non accessible :**
   - Vérifiez que `ollama serve` est en cours d'exécution
   - Vérifiez l'URL dans `OLLAMA_URL`

2. **Modèle non trouvé :**
   ```bash
   ollama pull adrienbrault/nous-hermes2pro:Q3_K_M
   ```

3. **Base de données corrompue :**
   ```bash
   rm crm_ecommerce.db  # Supprime et recrée au redémarrage
   ```

4. **Port déjà utilisé :**
   ```bash
   # Changer les ports
   uvicorn serveur:app --port 8001
   streamlit run dashboard.py --server.port 8502
   ```

## Licence

Ce projet est sous licence MIT. Voir le fichier [LICENSE](LICENSE) pour plus de détails.

## Contribution

Les contributions sont les bienvenues ! N'hésitez pas à :
- Signaler des bugs
- Proposer des améliorations
- Soumettre des pull requests
- Améliorer la documentation

## Auteurs

Développé pour BKC (Blockchain + Burger King Company) avec l'assistante virtuelle Isabelle.

## Support

Pour toute question ou problème :
1. Vérifiez la section Troubleshooting
2. Consultez les logs des serveurs
3. Vérifiez la configuration d'Ollama
4. Testez la connectivité des services
