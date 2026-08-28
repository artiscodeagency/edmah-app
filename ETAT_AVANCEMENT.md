# État d'avancement — EDMAH

**Dernière mise à jour :** 28 août 2026
**Périmètre :** l'application Django `edmah-app/`, seule version en production. Le dossier `frontend/` (maquette HTML/CSS/JS statique d'origine) n'est plus utilisé et n'a pas été modifié.

Ce document complète `RAPPORT_PROJET_EDMAH.md` (l'analyse et le plan initial) : il fait le point sur ce qui a été réellement construit et ce qui reste à faire.

---

## 1. Résumé exécutif

Le site est passé d'une maquette statique (aucune base de données, formulaires simulés) à une application Django fonctionnelle : back-office complet (Jazzmin), inscriptions et documents réellement enregistrés et sécurisés, espace apprenant avec progression et quiz notés côté serveur, contenus (formations, événements, blog, galerie) pilotés depuis l'admin, rôles candidat/apprenant/formateur/administrateur réellement différenciés, et site bilingue français/anglais fonctionnel. L'interface publique a été redessinée avec une identité visuelle propre à EDMAH (plus de dépendance à Bootstrap pour la mise en page), et l'administration utilise désormais Jazzmin avec la même charte bordeaux/or.

**Les phases 0 à 4 du plan initial (P0 — fondations, corrections front-end, CMS, inscription) sont terminées.** La phase 5 (catalogue et événements dynamiques, P1) est terminée. La phase 6 (espace apprenant, P1) est fonctionnelle de bout en bout, y compris l'accès différencié des formateurs. Les phases 7 et 8 (communauté/certification avancée, paiement, exploitation — P2) restent à faire, comme prévu au plan.

---

## 2. Ce qui est fait

### 2.1 Socle technique (P0 — Fondations)
- Projet Django 6.1 + DRF installés, 8 applications métier (`accounts`, `catalog`, `admissions`, `learning`, `events`, `content`, `communications`, `certificates`)
- Utilisateur personnalisé (`accounts.User`) avec rôles (candidat, apprenant, formateur, administrateur) — **rôles réellement différenciés**, voir §2.8
- Base de données migrée, modèles réels pour chaque entité métier (formation, session, inscription, événement, article, quiz, progression, certificat, message de contact, abonné newsletter…)
- Authentification (connexion, création de compte apprenant, déconnexion) avec formulaires stylés
- Fichiers d'inscription (photo d'identité, pièce d'état civil, documents complémentaires) stockés **hors du dossier public `/media/`**, servis uniquement via une vue réservée au personnel — vérifié qu'un visiteur non authentifié ou non membre du staff ne peut pas y accéder directement par URL
- 8 tests automatisés (inscription complète, refus de formation inconnue, champ obligatoire manquant, confidentialité des documents, inscription/désinscription à un événement, accès non autorisé à un cours, quiz réussi/échoué) — tous verts
- Cache-busting automatique des fichiers CSS/JS (`static_versioned`) basé sur la date de modification, pour que les mises à jour de design soient visibles immédiatement

### 2.2 Corrections et cohérence du front-end (P0)
- Aucun lien cassé (`inscription.html` vs `inscriptions.html`) ni page d'accueil dupliquée dans l'application Django — ce problème n'existait que dans l'ancien dossier `frontend/`, non utilisé
- Script commun (`main.js`) branché sur toutes les pages, jeton CSRF géré automatiquement sur tous les appels

### 2.3 Back-office — Jazzmin (P0)
- Toutes les entités gérables depuis `/admin/` : formations, sessions, catégories, événements, articles, galerie, FAQ, utilisateurs, dossiers d'inscription (avec actions "accepter / refuser / en cours"), modules de cours, quiz, questions, certificats
- **Administration migrée sur `django-jazzmin`**, entièrement personnalisée à la charte EDMAH : logo, icône propre à chaque application/modèle, page de connexion à deux volets (bordeaux + formulaire), barre latérale sombre avec état actif en or, formulaires en onglets horizontaux, mode clair/sombre
- **Accès différencié par rôle** : un formateur ne voit dans l'admin que ses propres cours et les modules qui en dépendent (détail au §2.8)

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

### 2.7 Identité visuelle
- Système de conception propre à EDMAH (`framework.css` : grille, boutons, formulaires, modales, cartes — sans dépendance à Bootstrap ; `navbar-footer.css` ; `style.css`)
- Barre de navigation reconstruite : aucun retour à la ligne aux largeurs intermédiaires, menu mobile en tiroir avec toutes les pages, bouton d'inscription, statut de connexion et sélecteur de langue
- Pied de page reconstruit avec le vrai logo EDMAH (plus l'icône cœur), plan du site, coordonnées, réseaux sociaux
- Animations et micro-interactions (défilement, survols, compte à rebours, lightbox, bascule mot de passe visible/masqué) en JavaScript natif
- Design audité avec la skill `ui-ux-pro-max` (accessibilité, contraste, typographie) — palette bordeaux/or et polices Playfair Display/Inter conservées à dessein, seuls les écarts réels (contraste d'un texte, annonce des erreurs aux lecteurs d'écran) ont été corrigés

### 2.8 Rôles et permissions — qui peut faire quoi
- **Candidat** : dépose un dossier d'inscription (`admissions.Inscription`), sans compte requis. Devient apprenant une fois son dossier accepté.
- **Apprenant** : compte avec accès à `/apprenant/` uniquement (tableau de bord, cours, quiz, notes) — aucun accès à `/admin/`.
- **Formateur** : a désormais **son interface** — c'est l'admin Jazzmin, mais restreinte à ce qui le concerne :
  - `accounts.User.role = 'formateur'` déclenche automatiquement `is_staff = True` et l'ajout au groupe **« Formateurs »** (permissions : gérer modules/ressources/quiz/questions/choix, consulter — sans modifier — les tentatives et progressions de ses apprenants)
  - Un cours (`learning.Course`) a maintenant un champ **`instructors`** (plusieurs formateurs possibles par cours) ; un formateur ne voit dans l'admin que les cours où il est instructeur, et seulement les modules/quiz qui en dépendent — vérifié : un formateur reçoit un **403** sur les autres sections (candidats, catalogue, événements…)
  - Le formateur **peut ajouter des leçons (modules), des ressources téléchargeables et des quiz** sur ses propres cours ; il ne peut pas créer de nouveau cours ni changer la formation associée (réservé à l'administrateur)
  - Compte de démonstration : `formateur.demo`
- **Administrateur** : accès complet à toutes les sections de l'admin, sans restriction.

### 2.9 Traduction français ↔ anglais (fonctionnelle)
- Les **296 chaînes** de l'interface publique (navigation, pages, formulaires, espace apprenant, e-mails de l'UI) sont désormais **traduites en anglais** et compilées (`locale/en/LC_MESSAGES/django.mo`)
- Le sélecteur FR/EN de la barre de navigation change réellement la langue affichée (testé : bascule de session + détection `Accept-Language`)
- Corrigé au passage : deux témoignages et une citation biblique dont l'échappement d'apostrophe cassait à la fois l'extraction des traductions et risquait de casser le JavaScript (guillemets simples remplacés par des gabarits littéraux/guillemets français)
- **Limite assumée** : le contenu saisi dans l'admin (noms de formations, catégories, articles de blog, FAQ…) reste dans la langue où il a été rédigé — ce n'est pas traduit automatiquement. Traduire ce contenu nécessiterait un champ par langue en base (ex. `django-modeltranslation`), non demandé à ce stade.

---

## 3. Ce qui reste à faire

### 3.1 Court terme — pour finaliser proprement le P1
- **Page de détail d'un événement** : la réservation se fait aujourd'hui depuis une fenêtre modale sur la liste ; une page dédiée par événement (comme pour les articles de blog) n'a pas été créée
- **Contenu de la page « À propos »** : mission, vision, équipe, témoignages restent en texte statique (aucun modèle de données prévu à ce stade — acceptable pour du contenu institutionnel, mais à confirmer)
- **Traduction du contenu éditorial** (formations, articles, FAQ...) — voir limite au §2.9
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
5. Un formateur doit-il pouvoir créer lui-même un nouveau cours/formation, ou cela doit-il rester réservé à l'administrateur ? (choix actuel : réservé à l'administrateur)

---

## 4. Accès de développement

```bash
cd edmah-app
.venv/Scripts/python.exe manage.py runserver
```

- Administration (Jazzmin) : `/admin/` — compte `admin` (mot de passe communiqué séparément)
- Compte apprenant de démonstration : `apprenant.demo`
- Compte formateur de démonstration : `formateur.demo` (accès admin restreint à son cours)
- Données de démonstration : `python manage.py seed_demo_data` (formations, événements, articles, modules de cours, un dossier accepté, un formateur assigné)
