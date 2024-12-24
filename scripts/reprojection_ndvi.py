# Importation des bibliothèques
import os

# Importation des fonctions
from functions import reproject_raster, split_bands

# Chemin vers le raster d"entrée
input_raster = "data_brut/Serie_temp_S2_ndvi.tif"
output_dir = "data_final"
dates = ["02-2022", "03-2022", "04-2022", "07-2022", "09-2022", "11-2022"]

# Crée le répertoire de sortie s"il n"existe pas
os.makedirs(output_dir, exist_ok=True)

# Reprojeter l"image en EPSG:3857
reprojected_raster = os.path.join(output_dir, "SerieTemp_NDVI_S2_3857.tif")
reproject_raster(input_raster, reprojected_raster, 3857)

# Séparer les bandes de l"image reprojetée
split_bands(reprojected_raster, output_dir, dates)
