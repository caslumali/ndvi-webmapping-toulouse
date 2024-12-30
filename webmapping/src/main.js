// Importation de Vue et des styles nécessaires
import { createApp } from "vue";
import "leaflet/dist/leaflet.css"; // Importation des styles de Leaflet
import "./style.css"; // Importation des styles personnalisés
import App from "./App.vue"; // Composant principal de l'application

// Création et montage de l'application Vue
createApp(App).mount("#app");
