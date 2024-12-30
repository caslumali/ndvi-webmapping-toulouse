import { defineConfig } from "vite"; // Importation de la configuration Vite
import vue from "@vitejs/plugin-vue"; // Importation du plugin Vue pour Vite

export default defineConfig({
  plugins: [vue()], // Activation du plugin Vue
  base: "./", // Chemin de base pour la production
  server: {
    port: 5173, // Définition du port local
  },
});
