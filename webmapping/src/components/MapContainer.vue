<template>
    <div id="map-container">
      <!-- La div qui contiendra la carte Leaflet -->
      <div id="map"></div>
    </div>
  </template>
  
  <script>
  import L from "leaflet";
  
  export default {
    name: "MapContainer",
  
    data() {
      return {
        // Carte Leaflet
        map: null,
  
        // URL GeoServer
        geoserverUrl: "https://www.geotests.net/geoserver/ows",
  
        // Fonds
        baseLayers: {},
        currentBaseLayer: null,
  
        // BD Forêt
        bdForetLayerName: "lima:Sample_BD_foret_3857",
        bdForetLayer: null,
        showBdForet: true,
  
        // NDVI mono-bande
        ndviLayerNames: [
          "lima:S2_NDVI_02-2022",
          "lima:S2_NDVI_03-2022",
          "lima:S2_NDVI_04-2022",
          "lima:S2_NDVI_07-2022",
          "lima:S2_NDVI_09-2022",
          "lima:S2_NDVI_11-2022",
        ],
        ndviLayers: [],
        showNdvi: false,
        selectedMonth: 0,
  
        /*
          Raster multi-bande invisible 
          => "lima:SerieTemp_NDVI_2022"
        */
        ndviMultiBandLayerName: "lima:SerieTemp_NDVI_2022",
      };
    },
  
    mounted() {
      // Initialisation
      this.initMap();
      this.addFixedLayers();
      this.initBdForet();
      this.initNdviLayers();
      this.addClickListener();
    },
  
    methods: {
      /*
        Création de la carte Leaflet
      */
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
  
        // Fond sombre (darkMatter)
        this.baseLayers.darkMatter = L.tileLayer(
          "https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png",
          {
            attribution: "&copy; OpenStreetMap contributors &copy; CARTO",
            subdomains: "abcd",
            maxZoom: 20,
          }
        );
  
        // Imagerie ESRI
        this.baseLayers.worldImagery = L.tileLayer(
          "https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
          {
            attribution: "Tiles © Esri, USGS, IGN",
          }
        );
  
        // Ajout du fond sombre
        this.currentBaseLayer = this.baseLayers.darkMatter;
        this.currentBaseLayer.addTo(this.map);
      },
  
      /*
        Ajoute l'emprise + emprise_inversee
      */
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
  
      /*
        BD Forêt
      */
      initBdForet() {
        this.bdForetLayer = L.tileLayer.wms(this.geoserverUrl, {
          layers: this.bdForetLayerName,
          format: "image/png",
          transparent: true,
        });
        if (this.showBdForet) {
          this.bdForetLayer.addTo(this.map);
        }
      },
  
      /*
        NDVI mono-bande : 6 couches
      */
      initNdviLayers() {
        this.ndviLayerNames.forEach((layerName) => {
          const layer = L.tileLayer.wms(this.geoserverUrl, {
            layers: layerName,
            format: "image/png",
            transparent: true,
          });
          this.ndviLayers.push(layer);
        });
      },
  
      /*
        Changer le fond de carte
      */
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
  
      /*
        BD Forêt ON/OFF
      */
      toggleBdForet(show) {
        this.showBdForet = show;
        if (show) {
          this.bdForetLayer.addTo(this.map);
        } else {
          this.map.removeLayer(this.bdForetLayer);
        }
      },
  
      /*
        NDVI ON/OFF
      */
      toggleNdvi(show) {
        this.showNdvi = show;
        this.updateNdviLayer();
      },
  
      /*
        Changement de mois NDVI
      */
      updateNdviMonth(monthIndex) {
        this.selectedMonth = monthIndex;
        this.updateNdviLayer();
      },
  
      /*
        Active la couche NDVI correspondante
      */
      updateNdviLayer() {
        // Retire toutes les couches NDVI
        this.ndviLayers.forEach((layer) => {
          this.map.removeLayer(layer);
        });
        // Ajoute celle du mois si NDVI coché
        if (this.showNdvi) {
          const currentLayer = this.ndviLayers[this.selectedMonth];
          currentLayer.addTo(this.map);
        }
      },
  
      /*
        Requête WMS GetFeatureInfo pour un layer + latlng
      */
      async doGetFeatureInfo(layerName, latlng) {
        const mapSize = this.map.getSize();
        const bounds = this.map.getBounds();
  
        // Projection en 3857
        const sw = this.map.options.crs.project(bounds.getSouthWest());
        const ne = this.map.options.crs.project(bounds.getNorthEast());
        const clickedPoint = this.map.options.crs.project(latlng);
  
        const minx = sw.x; 
        const miny = sw.y;
        const maxx = ne.x; 
        const maxy = ne.y;
        const width = mapSize.x; 
        const height = mapSize.y;
  
        // Pixel cliqué
        const i = Math.round(((clickedPoint.x - minx) / (maxx - minx)) * width);
        const j = Math.round(((maxy - clickedPoint.y) / (maxy - miny)) * height);
  
        const params = new URLSearchParams({
          service: "WMS",
          version: "1.1.1",
          request: "GetFeatureInfo",
          layers: layerName,
          query_layers: layerName,
          srs: "EPSG:3857",
          bbox: [minx, miny, maxx, maxy].join(","),
          width: width,
          height: height,
          x: i,
          y: j,
          info_format: "application/json",
        });
        const url = `${this.geoserverUrl}?${params.toString()}`;
  
        try {
          const resp = await fetch(url);
          if (!resp.ok) throw new Error("Erreur HTTP " + resp.status);
          return await resp.json();
        } catch (err) {
          console.error("Erreur doGetFeatureInfo", err);
          return null;
        }
      },
  
      /*
        addClickListener : on interroge
          1) BD Forêt -> 'Nom'
          2) Multi-bande -> 6 bands
          => On émet "ndvi-values" au parent
      */
        // ... on clique ...
      addClickListener() {
        this.map.on("click", async (e) => {
          const zoomLevel = this.map.getZoom();
          if (zoomLevel < 10) {
            // On n’émet que l’erreur
            this.$emit("ndvi-values", {
              errorMessage:
                "Veuillez zoomer davantage pour interroger les données.",
            });
            return;
          }
      
          // 1) Interroge BD Forêt
          let essence = "Essence inconnue";
          const bdForetInfo = await this.doGetFeatureInfo(
            this.bdForetLayerName,
            e.latlng
          );
          // On ne force pas "essence" si la BD Forêt est vide, 
          // c’est OK qu’elle reste "Essence inconnue" *s’il y a un pixel NDVI*
      
          // 2) Interroge le raster multi-bande
          const multiData = await this.doGetFeatureInfo(
            this.ndviMultiBandLayerName,
            e.latlng
          );
      
          // SI multiData est nul ou n’a pas de features => NDVI invalide
          if (!multiData || !multiData.features || !multiData.features.length) {
            this.$emit("ndvi-values", {
              errorMessage:
                "Zone sans données. Veuillez cliquer sur une zone contenant des pixels valides pour afficher le graphique !",
            });
            return; // IMPORTANT
          }
      
          // Récupération des bandes
          const props = multiData.features[0].properties;
          if (!props || props["Band1"] == null) {
            this.$emit("ndvi-values", {
              errorMessage:
                "Zone sans données. Veuillez cliquer sur une zone contenant des pixels valides pour afficher le graphique !",
            });
            return;
          }
      
          const bandValues = [
            props["Band1"],
            props["Band2"],
            props["Band3"],
            props["Band4"],
            props["Band5"],
            props["Band6"],
          ];
      
          // Cas NoData ou -9999
          if (
            bandValues[0] == null ||
            bandValues[0] === -9999 ||
            isNaN(bandValues[0])
          ) {
            this.$emit("ndvi-values", {
              errorMessage:
                "Zone sans données. Veuillez cliquer sur une zone contenant des pixels valides pour afficher le graphique !",
            });
            return;
          }
      
          // Sinon => tout est valide
          // On peut maintenant récupérer l’essence BDForêt
          // (si BDForêt est vide, ça reste “Essence inconnue”)
          if (
            bdForetInfo &&
            bdForetInfo.features &&
            bdForetInfo.features.length > 0 &&
            bdForetInfo.features[0].properties["Nom"]
          ) {
            essence = bdForetInfo.features[0].properties["Nom"];
          }
      
          // Émission normale : on envoie essence + tableau NDVI
          this.$emit("ndvi-values", {
            essence,
            values: bandValues,
          });
        });
      },
    },
  };
  </script>
  