# Rapport d'analyse et plan de réalisation — EDMAH

**Date d'analyse :** 24 août 2026  
**Périmètre analysé :** contenu du dossier projet uniquement. Aucune API, base de données ou configuration de déploiement n'est présente.

## 1. Résumé exécutif

EDMAH est le site d'une école de formation autour du mariage et de la vie familiale, avec une inspiration biblique. Le front-end dessine deux produits complémentaires :

1. un site public pour présenter l'école, ses formations, événements, articles et médias ;
2. un espace apprenant permettant de suivre des cours, répondre à des quiz, accéder à des ressources, prendre des notes et obtenir un certificat.

L'interface est déjà riche et les parcours attendus sont assez explicites. En revanche, le projet est actuellement une maquette HTML/CSS/JavaScript statique : les formulaires, les téléchargements, la progression des cours et les chargements de contenu utilisent des simulations. La priorité est donc de transformer ces parcours en fonctions réelles, en commençant par l'administration des contenus, l'inscription et l'espace apprenant.

## 2. État actuel

| Sujet | Constat |
|---|---|
| Technologies | Pages HTML statiques, CSS, JavaScript vanilla, Bootstrap 5, AOS et Font Awesome chargés depuis CDN. |
| Pages | Accueil, à propos, formations, cours, événements, galerie, blog, contact, inscription, certifications. |
| Serveur / données | Absents du dépôt. Les données affichées sont écrites directement dans les pages. |
| Intégrations prévues | `/api/newsletter`, `/api/contact`, `/api/register`, `/api/formations`, `/api/events`, `/api/blog` sont déclarées dans `main.js`. |
| Fonctionnalités réelles | Navigation, animations, filtrage local des listes, recherche locale d'articles, aperçu local de fichiers et quiz de démonstration. |
| Fonctionnalités simulées | Envoi contact/newsletter/inscription, pagination blog, chargement de cours, téléchargements, progression et certification. |

### Écarts et anomalies à corriger

- `home.html` et `index.html` sont des doublons exacts : une seule page d'accueil doit rester canonique.
- Plusieurs liens pointent vers `inscription.html`, fichier inexistant ; le fichier fourni est `inscriptions.html`. Ces liens concernent notamment la barre de navigation, les événements, les cours, la galerie et le contact.
- `main.js` contient la configuration et les fonctions API mais n'est inclus dans aucune page. Les scripts dupliqués dans les pages doivent être regroupés ou remplacés par ce socle commun.
- `certifications.html` affiche une interface de cours/quiz très proche de `cours.html`, et non un parcours de vérification ou de délivrance de certificat distinct. La règle métier de certification reste à préciser.
- Les médias de la galerie, la vidéo de présentation, la carte et les documents téléchargeables ne sont pas encore raccordés à des contenus de production.
- Il n'y a ni authentification, ni contrôle d'accès, ni stockage durable. Les informations personnelles et pièces justificatives du formulaire d'inscription exigent en conséquence un traitement sécurisé avant toute mise en ligne.

## 3. Fonctionnalités déduites du front-end

### A. Site public

| Domaine | Fonctions attendues | État front-end |
|---|---|---|
| Accueil | Présenter l'école, ses chiffres, formations et témoignages ; ouvrir une vidéo ; s'abonner à la newsletter. | Mise en page prête ; vidéo et newsletter simulées. |
| À propos | Publier mission, vision, histoire, valeurs, équipe et appel à l'inscription. | Présentation statique prête. |
| Formations | Consulter le catalogue, filtrer par catégorie, voir prix/durée/contenu et aller vers l'inscription avec pré-sélection. | Filtre local opérationnel ; catalogue statique. |
| Événements | Afficher l'événement à venir et les événements passés/futurs, filtrer par type, s'inscrire à un événement. | Filtre local ; inscription événement non implémentée et lien cassé. |
| Blog | Lister les articles, filtrer par catégorie, rechercher, paginer/charger davantage et s'abonner. | Filtre/recherche locale ; pagination, chargement et abonnement simulés. |
| Galerie | Filtrer photos, vidéos, événements et témoignages ; ouvrir une visionneuse, naviguer au clavier. | Fonctionnement local prêt ; contenus à gérer. |
| Contact | Afficher les coordonnées, FAQ, carte et envoyer une demande par sujet. | FAQ locale ; envoi simulé ; carte à paramétrer. |

### B. Conversion et inscription

| Fonction | Parcours attendu |
|---|---|
| Inscription à une formation | Formulaire en 4 étapes : identité et coordonnées, choix de formation/mode, dépôt de pièces, récapitulatif et acceptation des conditions. |
| Pré-sélection | Une formation choisie depuis le catalogue doit remplir automatiquement le formulaire. |
| Pièces jointes | Photo d'identité (JPEG/PNG, 2 Mo), document d'état civil (image/PDF, 5 Mo) et documents supplémentaires facultatifs (image/PDF, 5 Mo). |
| Contrôles | Champs obligatoires, email, formats/taille de fichiers, confirmation de conditions, prévention des doublons et statut d'inscription. |
| Suite attendue | Enregistrer la demande, notifier le demandeur et les administrateurs, permettre le traitement administratif et, si retenu, l'accès/paiement. |
| Inscription événement | Un parcours séparé est nécessaire : les liens transmettent déjà un identifiant d'événement, mais le formulaire actuel ne le traite pas. |

### C. Espace apprenant et certification

| Fonction | Comportement attendu |
|---|---|
| Compte et connexion | Un apprenant accède uniquement à ses formations et à sa progression. Un administrateur/formateur gère les contenus et les inscrits. |
| Cours par modules | Afficher le programme, verrouiller/déverrouiller les modules, charger le contenu correspondant et mémoriser la progression. |
| Quiz | Enregistrer tentatives, réponses, score et seuil de validation (80 % dans la maquette), puis débloquer la suite selon les règles. |
| Ressources | Mettre à disposition des documents réels, avec droit d'accès et suivi éventuel des téléchargements. |
| Notes | Sauvegarder automatiquement des notes privées et permettre leur export. |
| Forum | Publier une question ou expérience, afficher les échanges, modérer les contenus et notifier les réponses. |
| Certification | Vérifier les prérequis (modules, quiz et éventuelles règles pédagogiques), produire un certificat identifiable et permettre sa vérification publique. |

### D. Administration indispensable

L'interface publique implique un back-office, même s'il n'est pas encore dessiné :

- gérer les utilisateurs, rôles et accès ;
- créer/publier/archiver formations, modules, leçons, quiz et ressources ;
- gérer sessions, capacités, prix, modes, événements et inscriptions ;
- modérer blog, galerie, forum, commentaires et médias ;
- consulter, qualifier et répondre aux messages de contact ;
- traiter les dossiers d'inscription et leurs documents ;
- suivre newsletter, statistiques, progression, résultats et certificats.

## 4. Rôles et données principales

| Rôle | Capacités |
|---|---|
| Visiteur | Consulte les contenus publics, recherche/filtre, contacte EDMAH, s'abonne et dépose une demande. |
| Candidat | Suit son dossier, complète les informations demandées, reçoit les décisions et instructions de paiement. |
| Apprenant | Suit ses cours, ressources, quiz, notes, forum, progression et certificat. |
| Formateur | Gère ses contenus, ressources, évaluations et interactions pédagogiques selon les droits accordés. |
| Administrateur | Gère l'ensemble des contenus, utilisateurs, inscriptions, événements, certification, modération et reporting. |

Entités à prévoir : utilisateur, rôle, formation, session, module, leçon, ressource, inscription formation, pièce jointe, événement, inscription événement, article, catégorie/tag, média galerie, message contact, abonnement newsletter, quiz, question, tentative, progression, note, publication/réponse forum, certificat et paiement (si activé).

## 5. Priorisation et plan de travail

L'estimation ci-dessous est exprimée en effort de réalisation et suppose les contenus, règles pédagogiques, responsables métier et choix de paiement disponibles. Elle doit être affinée après cadrage.

| Phase | Priorité | Tâches | Résultat attendu | Effort indicatif |
|---|---:|---|---|---:|
| 0. Cadrage | P0 | Valider rôles, règles d'admission/certification, formations, événements, contenus initiaux, moyens de paiement, mentions légales et conservation des documents. | Cahier de règles et maquettes de flux validés. | 3–5 j |
| 1. Fondations | P0 | Choisir l'architecture, créer API/base de données, authentification, rôles, stockage sécurisé des fichiers, configuration des environnements, journalisation et sauvegardes. | Socle sécurisé, déployable et testable. | 8–12 j |
| 2. Corrections front-end | P0 | Corriger les liens `inscription(s).html`, supprimer le doublon accueil, brancher le script commun, rendre le site mobile/accesssible, remplacer les contenus factices prioritaires. | Parcours public cohérent sans lien cassé. | 3–5 j |
| 3. CMS / administration | P0 | Back-office pour formations, sessions, événements, blog, galerie, ressources, utilisateurs et dossiers. | Les équipes mettent à jour le site sans modifier le code. | 10–15 j |
| 4. Inscription et communication | P0 | API du formulaire multi-étapes, contrôle serveur des fichiers, suivi de statut, emails, contact et newsletter avec consentement. | Un candidat peut déposer et suivre un dossier fiable. | 8–12 j |
| 5. Catalogue et événements | P1 | Raccorder les catalogues/filtres/recherche/pagination aux données, ajouter détails et inscription événement. | Contenus dynamiques et réservations exploitables. | 5–8 j |
| 6. Espace apprenant | P1 | Tableau de bord, accès aux cours, progression persistante, ressources protégées, notes et quiz. | Apprentissage en ligne fonctionnel de bout en bout. | 12–18 j |
| 7. Communauté et certification | P2 | Forum modéré, règles de délivrance, génération/vérification de certificats. | Engagement et validation pédagogique traçables. | 8–12 j |
| 8. Paiement et exploitation | P2 | Intégrer le paiement validé, reçus, rapprochement, tableaux de bord, sauvegardes, monitoring, tests de charge et formation administrateurs. | Mise en production pilotable. | 8–14 j |

**Chemin critique MVP :** phases 0 à 4, puis la première formation complète de la phase 6. Les fonctions forum, certificat avancé et paiement peuvent être différées tant que le parcours d'inscription est géré manuellement.

## 6. Critères de réception du MVP

- Un visiteur peut consulter des contenus publiés, filtrer les formations/événements et rechercher les articles sans rechargement incohérent.
- Tous les appels à l'action d'inscription atteignent un parcours existant et préremplissent le contexte approprié (formation ou événement).
- Le serveur revalide tous les champs et fichiers ; les pièces ne sont jamais accessibles publiquement par simple URL.
- Un candidat reçoit une confirmation et un administrateur peut consulter, accepter, refuser ou demander un complément de dossier.
- Un administrateur peut créer et publier une formation, une session, un événement et un article depuis le back-office.
- Les fonctions contact et newsletter créent des enregistrements durables, avec gestion de l'erreur et consentement.
- Un apprenant autorisé peut consulter au moins une formation, passer un quiz et retrouver sa progression après reconnexion.
- Les tests couvrent au minimum l'inscription, les droits d'accès, l'import de fichiers et la validation du quiz.

## 7. Exigences transverses et risques

### Sécurité et conformité

- Les dossiers collectent date de naissance, adresse, téléphone et documents d'identité : chiffrement en transit, accès par rôle, antivirus/contrôle de type, limitation de taille, conservation limitée et traçabilité sont nécessaires.
- Définir les conditions d'utilisation, politique de confidentialité, consentement newsletter et procédure de suppression/export des données avant ouverture publique.
- Ne jamais faire reposer les droits d'accès, les prix, scores ou validations uniquement sur le navigateur.

### Qualité produit

- Prévoir une version mobile complète, navigation clavier, contrastes, libellés de formulaires et messages d'erreur accessibles.
- Remplacer les dépendances CDN non maîtrisées ou les sécuriser ; optimiser les images et définir une stratégie de sauvegarde/retour arrière.
- Centraliser les données et scripts afin d'éviter les divergences entre pages dupliquées.

### Décisions à prendre avant développement

1. Quel moyen de paiement doit être proposé (paiement manuel, Mobile Money, carte, virement) et à quel moment du dossier ?
2. Une inscription événement est-elle distincte d'une inscription formation, et est-elle payante ?
3. Quels sont les critères exacts de déblocage des modules et de délivrance des certificats ?
4. Qui publie et modère contenus, commentaires et forum ?
5. Quel contenu initial, quels documents et quelles vidéos peuvent être mis en ligne légalement ?

## 8. Recommandation de démarrage

Commencer par un atelier de cadrage court, puis construire un MVP administratif + inscription + première formation en ligne. Cette séquence sécurise les données sensibles, permet de publier les vrais contenus et évite de développer une plateforme de cours complète avant validation du parcours de recrutement et d'admission.
