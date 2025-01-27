// Importation de Vue et des styles nécessaires
import { createApp } from "vue";
import "leaflet/dist/leaflet.css"; // Importation des styles de Leaflet
import "./style.css"; // Importation des styles personnalisés
import App from "./App.vue"; // Composant principal de l'application
import '@fortawesome/fontawesome-free/css/all.min.css'; // Importantion des fonts pour le botton zoom in et out

// Création et montage de l'application Vue
createApp(App).mount("#app");
