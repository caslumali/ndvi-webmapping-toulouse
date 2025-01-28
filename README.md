

# **Analyse Spatio-Temporelle du NDVI - 2022**

## 🌍 **Contexte**
Ce projet a été réalisé dans le cadre de l'UE 902-1, **WebMapping**, du Master SIGMA 2024. Il vise à développer une solution complète de **webmapping** en appliquant les compétences acquises, couvrant tout le cycle de production :
1. Publication des données géospatiales via un serveur GeoServer.
2. Développement d'une interface web interactive pour la visualisation et l'analyse des données.



## 🌐 **Lien vers l'application**
[Accéder à l'application WebMapping](https://caslumali.alwaysdata.net/webmapping/)



## 🎯 **Objectifs**
- Mettre en œuvre un **webservice WMS** (avec GeoServer) à partir d'une carte géoréférencée produite dans l'UE 901-21 (*Traitement d'image satellite*).
- Consommer ce service via une interface web interactive développée avec des solutions **open source**.
- Offrir des fonctionnalités d'exploration et d'interrogation claires et ergonomiques.



## 🛠️ **Technologies utilisées**
### **Côté serveur :**
- **GeoServer :** Publication des données en services WMS standard.
- **Données publiées :**
  - **BD Forêt :** Représentation des forêts (style par défaut et par peuplement).
  - **NDVI (6 mois de 2022) :** Indices de végétation calculés à partir d'images Sentinel-2.
  - **Emprise et emprise inversée :** Couches pour contextualiser la carte.

### **Côté client :**
- **Framework :** Vue.js
- **Build tool :** Vite (pour le développement et la construction optimisée).
- **Bibliothèque de cartographie :** Leaflet.js
- **Node.js :** Gestion des dépendances et outils de développement.
- **Styles :** CSS personnalisé (mode sombre).
- **Composants principaux :**
  - `LayerControls.vue` : Contrôle des couches (activation/désactivation, slider NDVI).
  - `InfoBox.vue` : Présentation contextuelle des objectifs du projet.
  - `NdviChart.vue` : Graphiques interactifs NDVI.
  - `MapContainer.vue` : Gestion principale de la carte et des interactions.


## 🌟 **Fonctionnalités actuelles**
1. **Visualisation des couches géospatiales :**
   - BD Forêt (style par défaut et par peuplement).
   - NDVI (6 mois temporels de 2022).
2. **Interrogation des données :**
   - Affichage des types de essences.
   - Lecture des indices NDVI en cliquant sur un pixel de la carte.
3. **Interface interactive :**
   - Slider temporel pour changer les mois NDVI.
   - Navigation avec controle du zoom.
   - Présentation des informations dans une boîte INFO.
4. **Personnalisation de l'interface :**
   - Mode sombre pour les légendes et l'ensemble de l'application.


## 💡 **Choix méthodologiques**
1. **Pourquoi Vue.js ?**
   - Framework réactif et performant, facilitant le développement d'interfaces complexes et modulaires.
2. **Pourquoi Leaflet.js ?**
   - Solution légère et efficace pour la visualisation cartographique interactive, avec une large communauté pour le support et les extensions.
3. **Structuration du projet :**
   - Séparation des fonctionnalités en composants Vue pour une meilleure maintenabilité.
   - Utilisation de styles SCOPED dans les composants pour éviter les conflits.



## 🚀 **Perspectives d'amélioration**
1. **Ajout d'un localisateur de carte :**
   - Afficher une vue miniature pour situer la zone explorée.
2. **Export des résultats NDVI :**
   - Permettre l'export des données interrogées en format `.csv`.
3. **Comparaison multi-zones :**
   - Ajouter la possibilité d'interroger 3 à 5 zones simultanément et superposer leurs graphiques NDVI.
4. **Amélioration des légendes :**
   - Rendre la légende NDVI conforme au mode sombre des autres éléments.
5. **Optimisation de la performance :**
   - Charger dynamiquement les couches NDVI selon les besoins pour améliorer la vitesse.



## 🛠️ **Installation**
1. Clonez ce dépôt :
   ```bash
   git clone https://github.com/username/webmapping-project.git
   ```
2. Installez les dépendances :
   ```bash
   npm install
   ```
3. Lancez le serveur de développement :
   ```bash
   npm run dev
   ```
4. Accédez à l'application sur `http://localhost:5173/`.



## 📂 **Structure du projet**
```
├── src/
│   ├── components/
│   │   ├── InfoBox.vue          # Présentation des objectifs
│   │   ├── LayerControls.vue    # Contrôles des couches
│   │   ├── MapContainer.vue     # Carte interactive principale
│   │   ├── MapView.vue          # Combinaison carte + contrôles
│   │   └── NdviChart.vue        # Graphiques NDVI avec interactivé
│   ├── App.vue                  # Composant racine
│   ├── main.js                  # Point d'entrée principal
│   └── style.css                # Styles globaux
├── public/
│   └── index.html               # Fichier HTML principal
└── package.json                 # Dépendances npm
```


## 📜 **Crédits**
- **Encadrement pédagogique :** Laurent Jégou et Nicolas Lagarrigue.
- **Technologies open source :** Vue.js, Leaflet.js, GeoServer.
- **Contributeur principal :** Lucas Lima.

