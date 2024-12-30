<template>
    <div id="map-container">
      <div id="map"></div>
  
      <!-- Contrôle des couches -->
      <div id="layer-controls">
        <h3>Contrôle des Couches</h3>
        <!-- Sélection du fond -->
        <div>
          <label>
            <input type="radio" name="baseLayer" value="darkMatter" @change="changeBaseLayer('darkMatter')" checked />
            Fond Sombre
          </label>
          <label>
            <input type="radio" name="baseLayer" value="worldImagery" @change="changeBaseLayer('worldImagery')" />
            Imagerie Satellitaire
          </label>
        </div>
        <hr />
        <!-- Couches supplémentaires -->
        <div>
          <input type="checkbox" id="bdForet" v-model="showBdForet" />
          <label for="bdForet">BD Forêt</label>
        </div>
        <div>
          <input type="checkbox" id="ndvi" v-model="showNdvi" />
          <label for="ndvi">NDVI</label>
        </div>
        <!-- Barre des mois NDVI -->
        <div v-if="showNdvi" id="slider-container">
          <label for="slider">Sélectionnez le Mois :</label>
          <input type="range" id="slider" min="0" max="5" step="1" v-model="selectedMonth" />
          <span>{{ ndviMonths[selectedMonth] }}</span>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import L from "leaflet";
  
  export default {
    data() {
      return {
        map: null,
        ndviLayers: [],
        bdForetLayer: null,
        selectedMonth: 0,
        showNdvi: false,
        showBdForet: true,
        ndviMonths: [
          "Février 2022",
          "Mars 2022",
          "Avril 2022",
          "Juillet 2022",
          "Septembre 2022",
          "Novembre 2022",
        ],
        geoserverUrl: "https://www.geotests.net/geoserver/ows",
        baseLayers: {},
        currentBaseLayer: null,
      };
    },
    watch: {
      showBdForet(newVal) {
        if (newVal) {
          this.bdForetLayer.addTo(this.map);
        } else {
          this.map.removeLayer(this.bdForetLayer);
        }
      },
      showNdvi() {
        this.updateNdviLayer();
      },
      selectedMonth() {
        this.updateNdviLayer();
      },
    },
    mounted() {
      this.initMap();
      this.addFixedLayers();
      this.initBdForet();
      this.initNdviLayers();
    },
    methods: {
      initMap() {
        const centerCoordinates = [43.5615, 1.1194];
        const bounds = L.latLngBounds([43.24, 0.56], [43.92, 1.89]);
  
        this.map = L.map("map", {
          center: centerCoordinates,
          zoom: 10,
          maxBounds: bounds,
          maxZoom: 17,
          minZoom: 9,
        });
  
        // Couche de base par défaut
        this.baseLayers.darkMatter = L.tileLayer(
          "https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png",
          {
            attribution: '&copy; OpenStreetMap contributors &copy; CARTO',
            subdomains: "abcd",
            maxZoom: 20,
          }
        );
  
        this.baseLayers.worldImagery = L.tileLayer(
          "https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
          {
            attribution: "Tiles © Esri, Source: Esri, USGS, IGN",
          }
        );
  
        this.currentBaseLayer = this.baseLayers.darkMatter;
        this.currentBaseLayer.addTo(this.map);
      },
      changeBaseLayer(layerKey) {
        // Vérifie si une couche de fond est déjà active
        if (this.currentBaseLayer) {
            this.map.removeLayer(this.currentBaseLayer); // Retirer la couche de fond actuelle
        }

        // Met à jour la couche de fond actuelle avec la nouvelle sélectionnée
        this.currentBaseLayer = this.baseLayers[layerKey];
        this.currentBaseLayer.addTo(this.map); // Ajoute la nouvelle couche de fond à la carte

        // Ré-ajouter les couches fixes (Emprise et Emprise Inversée) après changement de fond
        this.addFixedLayers();

        // Ré-ajouter BD Forêt pour garantir qu'elle reste visible au-dessus du fond
        if (this.showBdForet && this.bdForetLayer) {
            this.map.removeLayer(this.bdForetLayer); // Supprime temporairement la couche
            this.bdForetLayer.addTo(this.map);      // La ré-ajoute pour la placer au-dessus
        }

        // Ré-ajouter NDVI si actif
        if (this.showNdvi) {
            this.updateNdviLayer();
        }
      },

      addFixedLayers() {
        L.tileLayer.wms(this.geoserverUrl, {
          layers: "lima:emprise_inversee",
          format: "image/png",
          transparent: true,
        }).addTo(this.map);
  
        L.tileLayer.wms(this.geoserverUrl, {
          layers: "lima:emprise",
          format: "image/png",
          transparent: true,
        }).addTo(this.map);
      },
      initBdForet() {
        this.bdForetLayer = L.tileLayer.wms(this.geoserverUrl, {
          layers: "lima:Sample_BD_foret_3857",
          format: "image/png",
          transparent: true,
        });
        if (this.showBdForet) {
          this.bdForetLayer.addTo(this.map);
        }
      },
      initNdviLayers() {
        const months = [
          "lima:S2_NDVI_02-2022",
          "lima:S2_NDVI_03-2022",
          "lima:S2_NDVI_04-2022",
          "lima:S2_NDVI_07-2022",
          "lima:S2_NDVI_09-2022",
          "lima:S2_NDVI_11-2022",
        ];
  
        months.forEach((layerName) => {
          const layer = L.tileLayer.wms(this.geoserverUrl, {
            layers: layerName,
            format: "image/png",
            transparent: true,
          });
          this.ndviLayers.push(layer);
        });
      },
      updateNdviLayer() {
        this.ndviLayers.forEach((layer) => this.map.removeLayer(layer));
        if (this.showNdvi) {
          this.ndviLayers[this.selectedMonth].addTo(this.map);
        }
      },
    },
  };
  </script>
  