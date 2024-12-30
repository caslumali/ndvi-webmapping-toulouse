<template>
    <!-- Conteneur principal pour la carte -->
    <div id="map"></div>
  </template>
  
  <script>
  import L from "leaflet";
  
  export default {
    mounted() {
      // Coordonnées de la zone d'intérêt
      const centerCoordinates = [43.5, 1.5]; // Centre de votre zone d'étude
      const zoomLevel = 12;
  
      // Définir les limites (bounding box) pour restreindre le zoom
      const bounds = L.latLngBounds(
        [43.0, 1.0], // Coin sud-ouest
        [44.0, 2.0]  // Coin nord-est
      );
  
      // Initialisation de la carte
      const map = L.map("map", {
        center: centerCoordinates,
        zoom: zoomLevel,
        maxBounds: bounds,
        maxZoom: 15,
        minZoom: 10,
      });
  
      // Ajout de la couche de base (fond OpenStreetMap)
      L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
        attribution: "&copy; OpenStreetMap contributors",
      }).addTo(map);
  
      // URL du GeoServer WMS
      const geoserverUrl = "https://www.geotests.net/geoserver/ows";
  
      // Ajout des couches Raster NDVI (une par mois, sans attribution)
      const ndviLayers = [
        "lima:S2_NDVI_02-2022",
        "lima:S2_NDVI_03-2022",
        "lima:S2_NDVI_04-2022",
        "lima:S2_NDVI_07-2022",
        "lima:S2_NDVI_09-2022",
        "lima:S2_NDVI_11-2022",
      ];
  
      ndviLayers.forEach((layerName) => {
        L.tileLayer.wms(geoserverUrl, {
          layers: layerName,
          format: "image/png",
          transparent: true,
        }).addTo(map);
      });
  
      // Ajout de la couche Série Temporelle (avec attribution spécifique)
      const serieTempLayer = L.tileLayer.wms(geoserverUrl, {
        layers: "lima:SerieTemp_NDVI_2022",
        format: "image/png",
        transparent: true,
        attribution: "Série Temporelle NDVI calculé à partir des images Sentinel 2",
      }).addTo(map);
  
      // Ajout des couches vectorielles
      const empriseLayer = L.tileLayer.wms(geoserverUrl, {
        layers: "lima:emprise",
        format: "image/png",
        transparent: true,
      }).addTo(map);
  
      const empriseInverseLayer = L.tileLayer.wms(geoserverUrl, {
        layers: "lima:emprise_inversee",
        format: "image/png",
        transparent: true,
      }).addTo(map);
  
      const bdForetLayer = L.tileLayer.wms(geoserverUrl, {
        layers: "lima:Sample_BD_foret_3857",
        format: "image/png",
        transparent: true,
        attribution: "BDForêt - IGN",
      }).addTo(map);
    },
  };
  </script>
  