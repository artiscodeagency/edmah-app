# EDMAH — École du Mariage Harmonieux (Application Django)

Bienvenue sur le dépôt principal de l'application web **EDMAH** (*École du Mariage Harmonieux*).

Ce projet combine un **site web vitrine public**, une **plateforme de gestion des admissions et inscriptions**, un **espace d'apprentissage en ligne (LMS)** avec quiz et progression, ainsi qu'un système de **génération et vérification publique de certificats**.

---

## 🛠️ Stack Technique

* **Langage** : Python 3.11+ (Python 3.13 recommandé)
* **Framework Web** : Django 5+
* **API REST** : Django REST Framework (DRF)
* **Frontend** : HTML5, CSS3, JavaScript Vanilla, Bootstrap 5 (Rendu via Django Templates)
* **Base de données** : SQLite (développement) / PostgreSQL (production)

---

## 📂 Architecture des Applications Django

L'application est découpée en **8 modules (applications Django)** indépendants :

1. **`accounts`** : Gestion des utilisateurs, des rôles (*Visiteur, Candidat, Apprenant, Formateur, Administrateur*), des profils et de l'authentification.
2. **`catalog`** : Catalogue des formations, catégories, sessions, tarifs et modalités.
3. **`admissions`** : Formulaire d'inscription multi-étapes, téléversement des pièces justificatives et suivi des statuts de dossier (*reçu, en cours, complément demandé, accepté, refusé*).
4. **`learning`** : Modules de cours, leçons, ressources pédagogiques protégées, quiz interactifs avec calcul de score serveur, notes privées et suivi de progression.
5. **`events`** : Gestion des événements, réservations et jauges de places.
6. **`content`** : Articles du blog, catégories, tags, FAQ et galerie multimédia (photos/vidéos).
7. **`communications`** : Messages du formulaire de contact, souscription à la newsletter et notifications par courriel.
8. **`certificates`** : Règles d'éligibilité, génération des certificats et vérification publique par code unique.

---

## 📁 Arborescence du Projet

```text
edmah-app/
├── .venv/                     # Environnement virtuel Python
├── .gitignore                 # Fichiers et dossiers exclus du contrôle de version
├── README.md                  # Documentation du projet
├── requirements.txt           # Dépendances Python du projet
├── manage.py                  # Script de gestion Django
├── edmah_project/             # Configuration globale du projet Django
├── templates/                 # Templates HTML frontend (avec base.html)
├── static/                    # Fichiers statiques CSS, JS et images
├── media/                     # Documents et fichiers déposés (stockage protégé)
├── accounts/                  # Application Gestion Utilisateurs & Authentification
├── catalog/                   # Application Catalogue Formations
├── admissions/                # Application Admissions & Dossiers
├── learning/                  # Application Cours, E-learning & Quiz
├── events/                    # Application Événements
├── content/                   # Application Contenus (Blog, Galerie, FAQ)
├── communications/            # Application Contact & Newsletter
└── certificates/              # Application Certifications
```

---

## 🚀 Guide d'Installation et Lancement Local

### 1. Prérequis
- Python 3.11 ou supérieur installé sur votre système.

### 2. Création et Activation de l'Environnement Virtuel
```bash
# Se placer dans le dossier edmah-app
cd edmah-app

# Créer l'environnement virtuel (si pas encore créé)
python -m venv .venv

# Activer l'environnement virtuel :
# Sur Windows (PowerShell) :
.\.venv\Scripts\Activate.ps1
# Sur Linux / macOS :
source .venv/bin/activate
```

### 3. Installation des Dépendances
```bash
pip install -r requirements.txt
```

### 4. Application des Migrations et Création du Superutilisateur
```bash
# Appliquer les migrations de base de données
python manage.py migrate

# Créer un compte administrateur Django Admin
python manage.py createsuperuser
```

### 5. Lancement du Serveur de Développement
```bash
python manage.py runserver
```
L'application sera accessible sur `http://127.0.0.1:8000/` et l'interface d'administration sur `http://127.0.0.1:8000/admin/`.

---

## 🔐 Sécurité et Fichiers Privés

Les documents d'identité et pièces justificatives téléversés par les candidats lors des inscriptions sont enregistrés dans le répertoire `media/` et sont protégés par le serveur Django : aucun document privé ne doit être accessible publiquement par simple URL directe.
