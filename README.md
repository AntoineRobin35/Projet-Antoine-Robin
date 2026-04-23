# Projets Python & Automatisation

Ce repository contient 4 projets personnels réalisés dans un objectif d’apprentissage en Python, IA et automatisation.

---

## 1. Agent IA

Agent conversationnel utilisant l’API Gemini.

### Fonctionnement
- Analyse un prompt utilisateur
- Peut appeler des fonctions externes (tools)
- Retourne une réponse enrichie

### Outils disponibles
- `give_weather` : récupère la météo d’une ville à une heure donnée via une API météo
- `give_people` : estime le nombre d’habitants d’une ville selon une règle définie

### Objectif
Comprendre le fonctionnement des outils (function calling) dans une IA générative.

---

## 2. Application Tkinter

Application desktop développée avec Tkinter.

### Fonctionnalités
- Ajout manuel d’applications
- Stockage des données dans un fichier JSON
- Affichage des applications sous forme de boutons avec logo
- Lancement des applications depuis l’interface

### Objectif
Créer un launcher personnalisé et manipuler des interfaces graphiques en Python.

---

## 3. Création IA (Neural Network from scratch)

Implémentation manuelle de composants d’IA.

### Éléments implémentés
- Neurone avec activation sigmoïde
- MLP (réseau de neurones multicouche)
- Backpropagation simplifiée
- Tokenizer basique
- Embeddings aléatoires
- Mécanisme d’attention simplifié

### Objectif
Comprendre les bases internes des réseaux de neurones et des Transformers.

---

## 4. Workflow n8n - Automatisation de prospection

Workflow d’automatisation basé sur n8n et Apify.

### Fonctionnement
- Saisie via formulaire (type de recherche, zone, nombre d’entreprises)
- Scraping Google Maps via Apify
- Récupération et traitement des données
- Stockage dans Google Sheets
- Filtrage des doublons
- Mise à jour des statuts :
  - “Garder ?”
  - “Démarché ?”

### Objectif
Automatiser la prospection d’entreprises et structurer une base de données de leads.

---

## Stack utilisée
- Python
- Tkinter
- Google Gemini API
- n8n
- Apify
- Google Sheets API
