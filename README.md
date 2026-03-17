# NDVI WebMapping Toulouse

WebGIS application for exploring Sentinel-2 NDVI time series in the Toulouse region using Vue, Leaflet, and GeoServer.

![Vue.js](https://img.shields.io/badge/Vue.js-4FC08D?style=flat&logo=vuedotjs&logoColor=white)
![Leaflet](https://img.shields.io/badge/Leaflet-199900?style=flat&logo=leaflet&logoColor=white)
![GeoServer](https://img.shields.io/badge/GeoServer-4285F4?style=flat)
![Node.js](https://img.shields.io/badge/Node.js-339933?style=flat&logo=nodedotjs&logoColor=white)

---

## Overview

This project is a full-stack WebGIS application designed to explore monthly NDVI layers derived from Sentinel-2 imagery over the Toulouse region.

The application combines:

- a GeoServer backend publishing raster and vector layers as WMS
- a Vue frontend for interface logic
- Leaflet for interactive mapping
- temporal NDVI exploration through a month slider and pixel querying

---

## Main features

- visualization of monthly NDVI layers
- interactive temporal slider
- pixel-level NDVI querying
- chart display for selected locations
- BD Forêt context layers
- dark interface theme

---

## Tech stack

- **Vue.js** and **Vite**
- **Leaflet**
- **GeoServer**
- **Node.js**

---

## Repository structure

```text
ndvi-webmapping-toulouse/
|-- webmapping/
|   |-- src/
|   |-- public/
|   `-- package.json
|-- scripts_geotraitements/
`-- README.md
```

---

## Why this repo matters

This repository shows:

- WebGIS frontend development for geospatial exploration
- publication and consumption of geospatial web services
- interaction design for temporal raster data
- a practical bridge between remote sensing outputs and web visualization

---

## Context

This project was developed in the SIGMA MSc as a WebMapping exercise, but it remains a useful public prototype of a geospatial web interface.
