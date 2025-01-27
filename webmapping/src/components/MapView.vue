<template>
  <div id="map-view">
    <!-- Conteneur principal : la carte + les contrôles + le graphique NDVI -->
    <div class="main-container">
      
      <!-- La carte Leaflet -->
      <MapContainer
        ref="mapContainerRef"
        @ndvi-values="handleNdviValues"
      />

      <!-- Contrôles : fond de carte, BD Forêt, NDVI, slider -->
      <LayerControls
        @toggle-base-layer="handleToggleBaseLayer"
        @toggle-bd-foret="handleToggleBdForet"
        @toggle-bd-foret-styled="handleToggleBdForetStyled"
        @toggle-ndvi="handleToggleNdvi"
        @change-ndvi-month="handleChangeNdviMonth"
      />

      <!-- Graphique NDVI (affiché seulement si showChart = true) -->
      <!-- :key pour forcer la mise à jour quand essence/ndviValues/error changent -->
      <NdviChart
        v-if="showChart"
        :key="essenceName + JSON.stringify(ndviValues) + chartErrorMessage"
        :ndvi-values="ndviValues"
        :months="ndviMonths"
        :essence="essenceName"
        :errorMessage="chartErrorMessage"
        @close-chart="showChart = false"
      />
    </div>
  </div>
</template>

<script>
/*
  Composant parent qui orchestre :
    - La carte (MapContainer.vue),
    - Les contrôles (LayerControls.vue),
    - Le graphique NDVI (NdviChart.vue).

  Quand on clique sur la carte, MapContainer émet "ndvi-values".
  MapView gère la logique d'erreur ou de success pour les valeurs NDVI 
  et affiche NdviChart en conséquence.
*/

import MapContainer from "./MapContainer.vue";
import LayerControls from "./LayerControls.vue";
import NdviChart from "./NdviChart.vue";

export default {
  name: "MapView",

  components: {
    MapContainer,
    LayerControls,
    NdviChart,
  },

  data() {
    return {
      // Affiche ou non le composant NdviChart
      showChart: false,

      // Valeurs NDVI récupérées (6 mois)
      ndviValues: [],

      // Nom de l'essence (BD Forêt)
      essenceName: "",

      // Noms des 6 mois (affichage X)
      ndviMonths: [
        "Févr.",
        "Mars",
        "Avr.",
        "Juil.",
        "Sept.",
        "Nov.",
      ],

      // Message d'erreur si pixel invalide
      chartErrorMessage: "",
    };
  },

  methods: {
    /*
      handleNdviValues(payload) est déclenché par l'événement 
      @ndvi-values émis par MapContainer quand on clique sur la carte.
    */
    handleNdviValues(payload) {
      // S'il y a un pixel invalide => payload.errorMessage
      if (payload.errorMessage) {
        // On stocke l'erreur
        this.chartErrorMessage = payload.errorMessage;
        // On vide NDVI + essence
        this.ndviValues = [];
        this.essenceName = "";
        // On montre le chart (qui affichera juste le message d'erreur)
        this.showChart = true;
      } else {
        // Sinon, c'est un pixel valide
        this.chartErrorMessage = "";
        this.essenceName = payload.essence || "Essence inconnue";
        this.ndviValues = payload.values || [];
        // On ouvre le graphique
        this.showChart = true;
      }
    },

    // Changement de fond
    handleToggleBaseLayer(baseLayerKey) {
      this.$refs.mapContainerRef.changeBaseLayer(baseLayerKey);
    },

    // BD Forêt ON/OFF
    handleToggleBdForet(show) {
      this.$refs.mapContainerRef.toggleBdForet(show);
    },

    // BD Forêt (par peuplement) ON/OFF
    handleToggleBdForetStyled(show) { 
      this.$refs.mapContainerRef.toggleBdForetStyled(show);
    },

    // NDVI ON/OFF
    handleToggleNdvi(show) {
      this.$refs.mapContainerRef.toggleNdvi(show);
    },

    // Mois NDVI
    handleChangeNdviMonth(selectedMonth) {
      this.$refs.mapContainerRef.updateNdviMonth(selectedMonth);
    },
  },
};
</script>
