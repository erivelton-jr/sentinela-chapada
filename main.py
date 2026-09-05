import logging
from src.extract import extract_fire_data, get_bbox
from src.geo_filter import filter_parna_chapada
from src.load import load_fire_data
from config.logger_config import setup_logging

setup_logging()
logging.getLogger(__name__)

def pipeline():
    try:
        logging.info("ETAPA 1: EXTRACT")

        sw, ne = get_bbox()
        extract = extract_fire_data(sw, ne)

        logging.info("ETAPA 2: FILTER")

        df = filter_parna_chapada(extract)

        logging.info("ETAPA 3: LOAD")

        load_fire_data(df)

        logging.info("PIPELINE FINALIZADO COM SUCESSO")

    except Exception as e:
        logging.exception("Erro durante execução do pipeline", e)


if __name__ == "__main__":
    pipeline()