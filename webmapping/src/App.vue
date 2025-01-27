<template>
  <div id="app">
    <h1>Analyse spatio-temporelle du NDVI pour l'année 2022 avec Sentinel-2</h1>
    <MapView />
    <InfoBox v-if="showInfo" @close-info="showInfo = false" />
  </div>
</template>

<script>
import MapView from "./components/MapView.vue";
import InfoBox from "./components/InfoBox.vue";

export default {
  name: "App",
  components: {
    MapView,
    InfoBox,
  },
  data() {
    return {
      showInfo: true, // Afficher INFO au chargement
    };
  },
};
</script>