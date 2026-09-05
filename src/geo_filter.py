import geopandas as gpd
from pathlib import Path
import logging

BASE_DIR = Path(__file__).resolve().parent.parent
logging.getLogger(__name__)

def load_boundary(kml):
    """
    Carrega o arquivo KML do Parque Nacional da Chapada Diamantina e retorna um GeoDataFrame.
    """
    gdf = gpd.read_file(kml).union_all()
    logging.info(f"Polígono carregado do arquivo KML")
    return gdf


def filter_parna_chapada(df,
                      kml=BASE_DIR / 'data' / 'shapefile' / 'PARNA_Chap_Diamantina.kml'):
    """
    Filtra os dados de queimadas para incluir apenas aqueles dentro do polígono.
    """

    #Carrega o poligono
    polygons = load_boundary(kml)

    # Converte o df para GeoDataFrame
    gdf = gpd.GeoDataFrame(df,
                           geometry=gpd.points_from_xy(df['longitude'],df['latitude']),
                           crs="EPSG:4326")

    # Filtra os pontos que estão dentro do polígono
    gdf_filtered = gdf.geometry.within(polygons)
    df_filtred = gdf[gdf_filtered].drop(columns='geometry')

    return df_filtred



