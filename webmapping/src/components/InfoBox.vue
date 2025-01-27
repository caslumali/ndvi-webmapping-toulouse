<!-- src/components/InfoBox.vue -->
<template>
    <div class="info-box">
      <h4>À propos de l'application.</h4>
      <p>
        Application créée comme projet final de la UE902_1 Webmapping du Master SIGMA UT2/ENSAT.
      </p>
      <p>
        Cette carte permet d'explorer les valeurs de NDVI pour différentes essences forestières en 2022.
      </p>
      <ul>
        <li>Activer/désactiver les couches géospatiales : <strong>BD Forêt</strong> et <strong>NDVI</strong>.</li>
        <li>Explorer les données temporelles du NDVI pour 2022 avec le <strong>slider</strong>.</li>
        <li>Cliquer sur une zone pour voir les types de forêts et indices NDVI dans un graphique interactif.</li>
      </ul>
      <p class="author">
        Créé par : <strong>Lucas Lima</strong>
      </p>
      <p class="note">
        <strong>Note :</strong> Certaines zones ne contiennent pas de données NDVI. Veuillez zoomer pour les analyser.
      </p>
      <button @click="closeInfo">Fermer</button>
    </div>
</template>

<script>
export default {
  name: "InfoBox",
  methods: {
    closeInfo() {
      this.$emit("close-info");
    },
  },
};
</script>
