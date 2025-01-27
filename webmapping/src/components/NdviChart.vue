<template>
    <div id="chart-container">
      <!-- HEADER commun -->
      <div class="chart-header">
        <!-- 
          Au lieu de v-if="!errorMessage", 
          on laisse la div chart-essence exister toujours 
          mais on affiche le texte seulement si pas d’erreur. 
        -->
        <div class="chart-essence">
          <template v-if="!errorMessage">
            Essence: {{ essence }}
          </template>
        </div>
  
        <!-- Bouton X (toujours visible à droite) -->
        <button 
          class="chart-close-btn" 
          @click="closeChart"
        >
          X
        </button>
      </div>
  
      <!-- 
        Si errorMessage => on l'affiche 
        Sinon => le canvas
      -->
      <div v-if="errorMessage" class="error-message">
        {{ errorMessage }}
      </div>
      <canvas v-else id="ndvi-chart"></canvas>
    </div>
  </template>
  
  <script>
  import Chart from "chart.js/auto";
  
  export default {
    name: "NdviChart",
  
    props: {
      essence: String,
      errorMessage: String,
      ndviValues: Array,
      months: Array,
    },
  
    data() {
      return {
        chartInstance: null,
      };
    },
  
    mounted() {
      // Si pas d'erreur => on crée le chart
      if (!this.errorMessage) {
        this.renderChart();
      }
    },
  
    watch: {
      // Si l’erreur apparaît ou disparaît
      errorMessage(newVal) {
        if (newVal) {
          // On détruit l’éventuel chart
          if (this.chartInstance) {
            this.chartInstance.destroy();
            this.chartInstance = null;
          }
        } else {
          // L'erreur a été enlevée => on recrée le chart
          this.renderChart();
        }
      },
      // Mise à jour des valeurs NDVI
      ndviValues(newVals) {
        if (this.chartInstance) {
          this.chartInstance.data.datasets[0].data = newVals;
          this.chartInstance.update();
        }
      },
    },
  
    methods: {
      closeChart() {
        this.$emit("close-chart");
      },
      renderChart() {
        const ctx = document.getElementById("ndvi-chart").getContext("2d");
        this.chartInstance = new Chart(ctx, {
          type: "line",
          data: {
            labels: this.months,
            datasets: [
              {
                label: "",
                data: this.ndviValues || [],
                borderColor: "#00d1b2",
                backgroundColor: "rgba(0, 209, 178, 0.2)",
                pointHoverRadius: 6,
                tension: 0.2,
              },
            ],
          },
          options: {
            responsive: true,
            interaction: { mode: "index", intersect: false },
            plugins: {
              legend: { display: false },
              tooltip: {
                enabled: true,
                backgroundColor: "rgba(0, 0, 0, 0.7)",
                titleColor: "#fff",
                bodyColor: "#fff",
              },
            },
            scales: {
              x: {
                ticks: {
                  color: "#ccc",
                  maxRotation: 45,
                  minRotation: 45,
                },
              },
              y: {
                min: 0.3,
                max: 1,
                ticks: { color: "#ccc" },
                  title: {
                    display: true,
                    text: "Valeurs du NDVI",
                    color: "#ccc",
                    padding: { top: 5, bottom: 5 },
                },
              },
            },
          },
        });
      },
    },
  };
  </script>
  