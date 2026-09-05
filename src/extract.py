import os
import geopandas as gpd
import pandas as pd
import requests
import logging
from io import StringIO
from pathlib import Path
import hashlib

logging.getLogger(__name__)

BASE_DIR = Path(__file__).resolve().parent.parent

def generate_fire_id(row):
    """
    Gera um id para cada fogo coletado
    """
    identificador = (
        f"{row['latitude']:.6f}|"
        f"{row['longitude']:.6f}|"
        f"{row['acq_date']}|"
        f"{row['acq_time']}|"
        f"{row['satellite']}"
    )

    hash_id = hashlib.sha256(
        identificador.encode("utf-8")
    ).hexdigest()[:16]

    return f"FIRMS-{hash_id}"


# coletar bounding box para leitura na api
def get_bbox(kml=BASE_DIR / 'data' / 'shapefile' / 'PARNA_Chap_Diamantina.kml'):
    """
    Gera um bounding box para cada fogo coletado.
    """

    coord = gpd.read_file(kml)

    sw = [coord.total_bounds[1], coord.total_bounds[0]]
    ne = [coord.total_bounds[3], coord.total_bounds[2]]

    return sw, ne

def extract_fire_data(sw, ne):
    API_KEY = os.getenv('FIRMS_API_KEY')
    SENSORS = ['MODIS_NRT',
               'VIIRS_NOAA20_NRT',
               'VIIRS_NOAA21_NRT',
               'VIIRS_SNPP_NRT']

    bbox = f"{sw[1]},{sw[0]},{ne[1]},{ne[0]}"

    dados = []

    for sensor in SENSORS:
        url = f"https://firms.modaps.eosdis.nasa.gov/api/area/csv/{API_KEY}/{sensor}/{bbox}/5"

        logging.info(f"COLETANDO DADOS DO SATELITE: {sensor}")

        try:
            response = requests.get(url)
            response.raise_for_status()  # Verifica se a requisição foi bem-sucedida

            #verifica se o sensor encontrou algum dado
            if response.text.strip() == "":
                logging.info(f"NENHUM DADO ENCONTRADO NO SATELITE: {sensor}")
                continue

            df = pd.read_csv(StringIO(response.text))
            df['sensor'] = sensor
            dados.append(df)

            logging.info(f"total de dados encontrados: {len(df)}")
        except Exception as e:
            logging.error(f"ERRO AO COLETAR DADOS DO SATELITE {sensor}: {e}")

    if dados:
        df = pd.concat(dados)
        df['fire_id'] = df.apply(generate_fire_id, axis=1)
        return df
