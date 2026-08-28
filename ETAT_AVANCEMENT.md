# État d'avancement — EDMAH

**Dernière mise à jour :** 28 août 2026
**Périmètre :** l'application Django `edmah-app/`, seule version en production. Le dossier `frontend/` (maquette HTML/CSS/JS statique d'origine) n'est plus utilisé et n'a pas été modifié.

Ce document complète `RAPPORT_PROJET_EDMAH.md` (l'analyse et le plan initial) : il fait le point sur ce qui a été réellement construit et ce qui reste à faire.

---

## 1. Résumé exécutif

Le site est passé d'une maquette statique (aucune base de données, formulaires simulés) à une application Django fonctionnelle : back-office complet, inscriptions et documents réellement enregistrés et sécurisés, espace apprenant avec progression et quiz notés côté serveur, contenus (formations, événements, blog, galerie) pilotés depuis l'admin. L'interface publique et l'interface d'administration ont toutes deux été redessinées avec une identité visuelle propre à EDMAH (plus de dépendance à Bootstrap pour la mise en page).

**Les phases 0 à 4 du plan initial (P0 — fondations, corrections front-end, CMS, inscription) sont terminées.** La phase 5 (catalogue et événements dynamiques, P1) est terminée. La phase 6 (espace apprenant, P1) est fonctionnelle de bout en bout sur son chemin principal. Les phases 7 et 8 (communauté/certification avancée, paiement, exploitation — P2) restent à faire, comme prévu au plan.

---

## 2. Ce qui est fait

### 2.1 Socle technique (P0 — Fondations)
- Projet Django 6.1 + DRF installés, 8 applications métier (`accounts`, `catalog`, `admissions`, `learning`, `events`, `content`, `communications`, `certificates`)
- Utilisateur personnalisé (`accounts.User`) avec rôles (candidat, apprenant, formateur, administrateur)
- Base de données migrée (9 migrations), modèles réels pour chaque entité métier (formation, session, inscription, événement, article, quiz, progression, certificat, message de contact, abonné newsletter…)
- Authentification (connexion, création de compte apprenant, déconnexion) avec formulaires stylés
- Fichiers d'inscription (photo d'identité, pièce d'état civil, documents complémentaires) stockés **hors du dossier public `/media/`**, servis uniquement via une vue réservée au personnel — vérifié qu'un visiteur non authentifié ou non membre du staff ne peut pas y accéder directement par URL
- 8 tests automatisés (inscription complète, refus de formation inconnue, champ obligatoire manquant, confidentialité des documents, inscription/désinscription à un événement, accès non autorisé à un cours, quiz réussi/échoué) — tous verts
- Cache-busting automatique des fichiers CSS/JS (`static_versioned`) basé sur la date de modification, pour que les mises à jour de design soient visibles immédiatement

### 2.2 Corrections et cohérence du front-end (P0)
- Aucun lien cassé (`inscription.html` vs `inscriptions.html`) ni page d'accueil dupliquée dans l'application Django — ce problème n'existait que dans l'ancien dossier `frontend/`, non utilisé
- Script commun (`main.js`) branché sur toutes les pages, jeton CSRF géré automatiquement sur tous les appels

### 2.3 Back-office / CMS (P0)
- Toutes les entités gérables depuis `/admin/` : formations, sessions, catégories, événements, articles, galerie, FAQ, utilisateurs, dossiers d'inscription (avec actions "accepter / refuser / en cours"), modules de cours, quiz, questions, certificats
- **Interface d'administration entièrement personnalisée** : logo et couleurs EDMAH (bordeaux/or), typographie Playfair Display/Inter, page de connexion à l'image du site, boutons et filtres redessinés, thème sombre assorti (le bouton clair/sombre/auto de Django fonctionne avec la palette EDMAH dans les deux modes)

### 2.4 Inscription et communication (P0)
- Formulaire d'inscription en 4 étapes réellement fonctionnel : validation serveur des champs, des types et tailles de fichiers (photo ≤ 2 Mo, documents ≤ 5 Mo), envoi d'un e-mail de confirmation au candidat et de notification à l'équipe (backend console en développement)
- Formulaire de contact et newsletter : enregistrement réel en base, retour d'erreur géré
- FAQ affichée sur la page contact, alimentée depuis l'admin

### 2.5 Catalogue et événements (P1)
- Formations, catégories et mise en avant pilotées par la base de données (plus de contenu en dur)
- Page événements : bannière avec compte à rebours en direct sur le prochain événement, réservation en ligne (modale) enregistrée en base, distinction événements à venir / passés
- Blog : recherche, filtre par catégorie et pagination réels, articles populaires en barre latérale
- Galerie : filtrage par catégorie et visionneuse (lightbox) avec navigation clavier, sur photos et vidéos

### 2.6 Espace apprenant (P1)
- Tableau de bord listant les formations pour lesquelles le dossier de l'apprenant a été accepté
- Déverrouillage séquentiel des modules, quiz noté côté serveur (seuil configurable, 80 % par défaut), progression persistée et retrouvée à la reconnexion
- Notes personnelles sauvegardées automatiquement par module
- Délivrance automatique du certificat quand tous les modules d'une formation sont validés
- Vérification publique d'un certificat par son code

### 2.7 Identité visuelle (refonte complète)
- Système de conception propre à EDMAH (`framework.css` : grille, boutons, formulaires, modales, cartes — sans dépendance à Bootstrap ; `navbar-footer.css` ; `style.css`)
- Barre de navigation reconstruite : aucun retour à la ligne aux largeurs intermédiaires, menu mobile en tiroir avec toutes les pages, bouton d'inscription, statut de connexion et sélecteur de langue
- Pied de page reconstruit avec le vrai logo EDMAH (plus l'icône cœur), plan du site, coordonnées, réseaux sociaux
- Animations et micro-interactions (défilement, survols, compte à rebours, lightbox, bascule mot de passe visible/masqué) en JavaScript natif
- Vérifié en navigateur, ordinateur et mobile, sur les pages principales (accueil, formations, événements, galerie, blog, contact, connexion, inscription-compte, tableau de bord apprenant)

---

## 3. Ce qui reste à faire

### 3.1 Court terme — pour finaliser proprement le P1
- **Page de détail d'un événement** : la réservation se fait aujourd'hui depuis une fenêtre modale sur la liste ; une page dédiée par événement (comme pour les articles de blog) n'a pas été créée
- **Contenu de la page « À propos »** : mission, vision, équipe, témoignages restent en texte statique (aucun modèle de données prévu à ce stade — acceptable pour du contenu institutionnel, mais à confirmer)
- **Traductions anglaises** : le sélecteur de langue FR/EN fonctionne, mais les 330 chaînes extraites côté anglais ne sont pas encore traduites (`locale/en/LC_MESSAGES/django.po`)
- **Ressources de cours** : le modèle existe (documents téléchargeables par module) mais aucun fichier réel n'a été déposé pour les modules de démonstration

### 3.2 Restant du plan initial — Phase 7 (P2, communauté et certification avancée)
- **Forum** : non commencé (aucun modèle, aucune vue) — publication, modération, notifications de réponse
- **Règles de certification avancées** : la règle actuelle est simple (tous les modules validés). Des règles pédagogiques plus fines (ex. délai minimum, évaluation formateur) restent à définir avec l'équipe métier puis à implémenter
- **Génération de certificat en PDF téléchargeable** : seul un enregistrement en base + vérification par code existent aujourd'hui, pas de document PDF généré

### 3.3 Restant du plan initial — Phase 8 (P2, paiement et exploitation)
- **Paiement** : aucun moyen n'est intégré ; un dossier accepté est aujourd'hui traité manuellement par l'équipe (choix assumé faute d'arbitrage sur le moyen de paiement — Mobile Money, carte, virement)
- **Durcissement production** : `DEBUG=True`, clé secrète Django en dur dans `settings.py`, base SQLite, hôtes autorisés limités à `localhost` — à corriger avant toute mise en ligne réelle (variables d'environnement, `DEBUG=False`, base PostgreSQL, domaine réel, HTTPS)
- **Envoi d'e-mails réel** : le backend est actuellement "console" (les e-mails s'affichent dans les journaux du serveur, ils ne partent pas réellement) ; à brancher sur un fournisseur SMTP/transactionnel
- **Sauvegardes, supervision, tests de charge, formation des administrateurs** : non entamés

### 3.4 Décisions métier encore en attente
Ces questions, déjà soulevées dans le rapport initial, conditionnent une partie du travail restant :
1. Quel moyen de paiement, et à quel moment du parcours ?
2. Les règles précises de déblocage des modules et de délivrance du certificat
3. Qui publie et modère le futur forum
4. Mentions légales, politique de confidentialité et conditions d'utilisation (liens présents en pied de page mais pointent vers des pages non créées)

---

## 4. Accès de développement

```bash
cd edmah-app
.venv/Scripts/python.exe manage.py runserver
```

- Administration : `/admin/` — compte `admin` (mot de passe communiqué séparément)
- Compte apprenant de démonstration : `apprenant.demo`
- Données de démonstration : `python manage.py seed_demo_data` (formations, événements, articles, modules de cours, un dossier accepté)
