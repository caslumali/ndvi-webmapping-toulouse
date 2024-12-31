<template>
  <!-- Conteneur principal de l'application -->
  <div id="app">
    <!-- Titre de l'application -->
    <h1>Analyse spatio-temporelle du NDVI pour l'année 2022 avec Sentinel-2</h1>
    <!-- Inclusion du composant MapView -->
    <MapView />
  </div>
</template>

<script>
  import MapView from "./components/MapView.vue";

  export default {
    components: {
      MapView, // Déclaration du composant de la carte
    },
  };
</script>
