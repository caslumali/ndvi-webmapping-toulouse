<template>
  <div id="layer-controls">
    <h3>Contrôle des couches</h3>

    <!-- Choix du fond de carte -->
    <div>
      <label>
        <input
          type="radio"
          name="baseLayer"
          value="darkMatter"
          @change="changeBaseLayer('darkMatter')"
          checked
        />
        Carto Sombre
      </label>
      <label>
        <input
          type="radio"
          name="baseLayer"
          value="worldImagery"
          @change="changeBaseLayer('worldImagery')"
        />
        Esri Satellite
      </label>
    </div>

    <hr />

    <!-- BD Forêt -->
    <div>
      <input
        type="checkbox"
        id="bdForet"
        v-model="localShowBdForet"
        @change="toggleBdForet"
      />
      <label for="bdForet">BD Forêt</label>

      <div v-if="localShowBdForet" class="legend">
        <!-- Légende BD Forêt, texte noir (fontColor:0x000000) -->
        <img
          :src="bdForetLegendUrl"
          alt="Légende BD Forêt"
          class="legend-image"
        />
      </div>
    </div>

    <!-- NDVI -->
    <div>
      <input
        type="checkbox"
        id="ndvi"
        v-model="localShowNdvi"
        @change="toggleNdvi"
      />
      <label for="ndvi">NDVI</label>

      <div v-if="localShowNdvi" class="legend">
        <!-- Légende NDVI, dépend du mois sélectionné (texte noir) -->
        <img
          :src="ndviLegendUrl + '&t=' + Date.now()"
          class="legend-image"
          alt="Légende NDVI"
        />
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
  </div>
</template>

<script>
/*
  Composant Vue qui gère :
  - La sélection du fond (radio)
  - L'activation BD Forêt / NDVI (checkbox)
  - Le slider NDVI (mois)
  - Les légendes WMS (BD Forêt, NDVI) avec paramètre "fontColor=0x000000" pour voir les chiffres
*/

export default {
  name: "LayerControls",

  data() {
    return {
      localShowBdForet: true,    // On stocke en local l'état BD Forêt
      localShowNdvi: false,      // On stocke en local l'état NDVI
      selectedMonth: 0,          // Mois NDVI

      // Noms des mois (pour affichage)
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
    // URL Geoserver
    geoserverUrl() {
      return "https://www.geotests.net/geoserver/ows";
    },

    // Nom de la couche BD Forêt
    bdForetLayerName() {
      return "lima:Sample_BD_foret_3857";
    },

    /*
      URL de GetLegendGraphic pour BD Forêt
      On force backgroundColor:0x333333, 
      ET fontColor:0x000000 (texte noir)
    */
    bdForetLegendUrl() {
      return (
        this.geoserverUrl +
        `?service=WMS&request=GetLegendGraphic&format=image/png` +
        `&layer=${this.bdForetLayerName}` +
        `&LEGEND_OPTIONS=fontColor:0x000000;backgroundColor:0x333333;forceLabels:off;forceTitles:off`
      );
    },

    /*
      URL de GetLegendGraphic pour NDVI (dépend du selectedMonth)
      Même principe : texte noir
    */
    ndviLegendUrl() {
      // On associe l'indice de selectedMonth à une couche NDVI
      const ndviLayerNames = [
        "lima:S2_NDVI_02-2022",
        "lima:S2_NDVI_03-2022",
        "lima:S2_NDVI_04-2022",
        "lima:S2_NDVI_07-2022",
        "lima:S2_NDVI_09-2022",
        "lima:S2_NDVI_11-2022",
      ];
      const currentLayer = ndviLayerNames[this.selectedMonth];

      return (
        this.geoserverUrl +
        `?service=WMS&request=GetLegendGraphic&format=image/png` +
        `&layer=${currentLayer}` +
        `&LEGEND_OPTIONS=fontColor:0x000000;backgroundColor:0x333333;forceLabels:on;forceTitles:on`
      );
    },
  },

  methods: {
    /* Émet un événement pour changer le fond de carte */
    changeBaseLayer(layerKey) {
      this.$emit("toggle-base-layer", layerKey);
    },

    /* Émet un événement pour activer/désactiver BD Forêt */
    toggleBdForet() {
      this.$emit("toggle-bd-foret", this.localShowBdForet);
    },

    /* Émet un événement pour activer/désactiver NDVI */
    toggleNdvi() {
      this.$emit("toggle-ndvi", this.localShowNdvi);
    },

    /* Mise à jour du mois NDVI (slider) */
    updateNdviMonth() {
      this.$emit("change-ndvi-month", this.selectedMonth);
    },
  },
};
</script>
