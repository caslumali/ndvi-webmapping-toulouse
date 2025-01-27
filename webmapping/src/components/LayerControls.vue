<template>
  <!-- Conteneur principal des contrôles de couches -->
  <div id="layer-controls" class="layer-controls">
    <h3>Contrôle des couches</h3>

    <!-- BD Forêt -->
    <div>
      <label>
        <input
          type="checkbox"
          v-model="localShowBdForet"
          @change="handleBdForetChange"
        />
        BD Forêt
      </label>
      <div v-if="localShowBdForet" class="legend">
        <div class="legend-item">
          <span class="legend-color" style="background-color: #009067;"></span>
        </div>
      </div>
    </div>

    <!-- BD Forêt (par peuplement) -->
    <div>
      <label>
        <input
          type="checkbox"
          v-model="localShowBdForetStyled"
          @change="handleBdForetStyledChange"
        />
        BD Forêt (par peuplement)
      </label>
      <div v-if="localShowBdForetStyled" class="legend">
        <div class="legend-item">
          <span class="legend-color" style="background-color: #33a02c;"></span>
          <span class="legend-label">Résineux</span>
        </div>
        <div class="legend-item">
          <span class="legend-color" style="background-color: #b0ad00;"></span>
          <span class="legend-label">Feuillus</span>
        </div>
        <div class="legend-item">
          <span class="legend-color" style="background-color: #eea83f;"></span>
          <span class="legend-label">Mélanges (résineux et feuillus)</span>
        </div>
      </div>
    </div>

    <!-- NDVI -->
    <div>
      <label>
        <input
          type="checkbox"
          v-model="localShowNdvi"
          @change="toggleNdvi"
        />
        NDVI 2022
      </label>
      <div v-if="localShowNdvi" class="legend">
        <div class="legend-item">
          <img
            :src="ndviLegendUrl + '&t=' + Date.now()"
            alt="Légende NDVI"
            class="legend-image"
          />
        </div>
      </div>
    </div>

    <!-- Slider NDVI -->
    <div v-if="localShowNdvi" id="slider-container">
      <label for="slider">Sélectionnez le Mois :</label>
      <input
        type="range"
        id="slider"
        min="0"
        max="5"
        step="1"
        v-model="selectedMonth"
        @input="updateNdviMonth"
      />
      <span>{{ ndviMonths[selectedMonth] }}</span>
    </div>

    <!-- Boutons de Zoom In, Zoom Out et Reset Zoom -->
    <div class="zoom-controls">
      <!-- Bouton de Zoom In -->
      <button @click="zoomIn" class="zoom-button" aria-label="Zoomer">
        <i class="fas fa-plus"></i> <!-- Icone Font Awesome pour Zoom In -->
      </button>
      <!-- Bouton de Zoom Out -->
      <button @click="zoomOut" class="zoom-button" aria-label="Dézoomer">
        <i class="fas fa-minus"></i> <!-- Icone Font Awesome pour Zoom Out -->
      </button>
      <!-- Bouton de Reset Zoom -->
      <button @click="resetZoom" class="zoom-button reset-zoom-button" aria-label="Réinitialiser le Zoom">
        <i class="fas fa-home"></i> <!-- Icone Font Awesome para Reset Zoom -->
      </button>
    </div>
  </div>
</template>

<script>
export default {
  name: "LayerControls",
  data() {
    return {
      localShowBdForet: true, // BD Forêt initialement activé
      localShowBdForetStyled: false, // BD Forêt (par peuplement) désactivé par défaut
      localShowNdvi: false, // NDVI désactivé par défaut
      selectedMonth: 0, // Mois NDVI sélectionné
      ndviMonths: [
        "Février 2022",
        "Mars 2022",
        "Avril 2022",
        "Juillet 2022",
        "Septembre 2022",
        "Novembre 2022",
      ],
    };
  },
  computed: {
    geoserverUrl() {
      return "https://www.geotests.net/geoserver/ows";
    },
    bdForetLegendUrl() {
      return `${this.geoserverUrl}?service=WMS&request=GetLegendGraphic&format=image/png&layer=lima:Sample_BD_foret_3857&LEGEND_OPTIONS=fontColor:0x000000;backgroundColor:0x333333;forceLabels:off;`;
    },
    bdForetStyledLegendUrl() {
      return `${this.geoserverUrl}?service=WMS&request=GetLegendGraphic&format=image/png&layer=lima:Sample_BD_foret_3857&style=lima:Sample_BD_Foret_essences_style&LEGEND_OPTIONS=fontColor:0x000000;backgroundColor:0x333333;forceLabels:on;forceTitles:on;fontSize:50&height=100&width=160`;
    },
    ndviLegendUrl() {
      const ndviLayerNames = [
        "lima:S2_NDVI_02-2022",
        "lima:S2_NDVI_03-2022",
        "lima:S2_NDVI_04-2022",
        "lima:S2_NDVI_07-2022",
        "lima:S2_NDVI_09-2022",
        "lima:S2_NDVI_11-2022",
      ];
      const currentLayer = ndviLayerNames[this.selectedMonth];
      return `${this.geoserverUrl}?service=WMS&request=GetLegendGraphic&format=image/png&layer=${currentLayer}&LEGEND_OPTIONS=fontColor:0x000000;backgroundColor:0x333333;forceLabels:on;forceTitles:on;fontSize:12`;
    },
  },
  methods: {
    // Gère l'activation/désactivation de BD Forêt
    handleBdForetChange() {
      if (this.localShowBdForet) {
        this.localShowBdForetStyled = false; // Désactiver BD Forêt (par peuplement)
        this.$emit("toggle-bd-foret-styled", false); // Émettre la désactivation
      }
      this.$emit("toggle-bd-foret", this.localShowBdForet);
    },

    // Gère l'activation/désactivation de BD Forêt (par peuplement)
    handleBdForetStyledChange() {
      if (this.localShowBdForetStyled) {
        this.localShowBdForet = false; // Désactiver BD Forêt
        this.$emit("toggle-bd-foret", false); // Émettre la désactivation
      }
      this.$emit("toggle-bd-foret-styled", this.localShowBdForetStyled);
    },

    // Gère l'activation/désactivation de NDVI
    toggleNdvi() {
      this.$emit("toggle-ndvi", this.localShowNdvi);
    },

    // Met à jour le mois pour NDVI
    updateNdviMonth() {
      this.$emit("change-ndvi-month", this.selectedMonth);
    },

    // Méthode pour zoomer
    zoomIn() {
      // Émettre un événement 'zoom-in' vers le parent
      this.$emit("zoom-in");
    },

    // Méthode pour dézoomer
    zoomOut() {
      // Émettre un événement 'zoom-out' vers le parent
      this.$emit("zoom-out");
    },

    // Méthode pour réinitialiser le zoom
    resetZoom() {
      // Émettre un événement 'reset-zoom' vers le parent
      this.$emit("reset-zoom");
    },
  },
};
</script>

