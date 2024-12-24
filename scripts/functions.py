import os
from osgeo import gdal, osr

# Configuration GDAL
gdal.UseExceptions()


def reproject_raster(input_path, output_path, target_epsg):
    """
    Reprojeter un raster vers un système de coordonnées donné avec compression LZW,
    en format float32 et avec une valeur NoData définie à -9999.

    Args:
        input_path (str): Chemin vers le fichier raster d'entrée.
        output_path (str): Chemin pour enregistrer le raster reprojeté.
        target_epsg (int): EPSG du système de coordonnées cible.

    Raises:
        FileNotFoundError: Si le fichier raster d'entrée est introuvable.
        Exception: Si une erreur se produit lors de la reprojection.
    """
    # Ouvrir le raster d'entrée
    src = gdal.Open(input_path)
    if not src:
        raise FileNotFoundError(f"Fichier introuvable : {input_path}")

    # Créer le système de référence de destination
    target_proj = osr.SpatialReference()
    target_proj.ImportFromEPSG(target_epsg)

    # Options pour reprojeter en float32 et définir NoData à -9999
    options = gdal.WarpOptions(
        dstSRS=target_proj.ExportToWkt(),
        format="GTiff",
        outputType=gdal.GDT_Float32,
        srcNodata=None,
        dstNodata=-9999,
        resampleAlg=gdal.GRA_Cubic,
        creationOptions=["COMPRESS=LZW", "TILED=YES"]
    )

    # Appliquer la reprojection
    dst = gdal.Warp(output_path, src, options=options)
    if dst:
        print(
            f"Reprojection terminée avec float32 et NoData=-9999 : {output_path}")
    else:
        raise Exception("Erreur lors de la reprojection")

    # Fermer les fichiers
    src = None
    dst = None


def split_bands(input_path, output_directory, dates):
    """
    Séparer les bandes d'un raster en fichiers individuels avec la date dans le nom,
    en format float32, avec une compression LZW et NoData défini à -9999.

    Args:
        input_path (str): Chemin vers le fichier raster d'entrée.
        output_directory (str): Répertoire où enregistrer les bandes séparées.
        dates (list): Liste des dates correspondant à chaque bande.

    Raises:
        FileNotFoundError: Si le fichier raster d'entrée est introuvable.
        ValueError: Si le nombre de dates ne correspond pas au nombre de bandes.
    """
    # Ouvrir le raster d'entrée
    dataset = gdal.Open(input_path)
    if not dataset:
        raise FileNotFoundError(f"Fichier introuvable : {input_path}")

    # Obtenir le nombre de bandes
    band_count = dataset.RasterCount
    print(f"Nombre de bandes : {band_count}")

    # Vérifier que le nombre de dates correspond au nombre de bandes
    if len(dates) != band_count:
        raise ValueError(
            "Le nombre de dates ne correspond pas au nombre de bandes dans le raster."
        )

    for i in range(1, band_count + 1):  # Les bandes commencent à 1
        band = dataset.GetRasterBand(i)

        # Ajouter la date au nom de fichier
        date = dates[i - 1]  # Les indices de liste commencent à 0
        band_output_path = os.path.join(
            output_directory, f"S2_NDVI_{date}.tif"
        )

        # Créer un fichier de sortie pour chaque bande avec compression LZW
        driver = gdal.GetDriverByName("GTiff")
        out_raster = driver.Create(
            band_output_path,
            dataset.RasterXSize,
            dataset.RasterYSize,
            1,
            gdal.GDT_Float32,  # Définir le type de données en float32
            options=["COMPRESS=LZW", "TILED=YES"]
        )

        # Copier les données de la bande
        array = band.ReadAsArray()
        out_band = out_raster.GetRasterBand(1)
        out_band.WriteArray(array)

        # Définir NoData à -9999
        out_band.SetNoDataValue(-9999)
        out_raster.SetGeoTransform(dataset.GetGeoTransform())
        out_raster.SetProjection(dataset.GetProjection())
        out_raster.FlushCache()

        print(
            f"Bande {i} enregistrée avec float32 et NoData=-9999 : {band_output_path}")

    # Fermer le dataset
    dataset = None
