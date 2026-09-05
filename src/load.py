import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import logging
logging.getLogger(__name__)
load_dotenv()


def load_fire_data(df):
    """
    Insere os dados do DataFrame na tabela fire_detections
    do banco PostgreSQL/PostGIS.

    Args:
        df: DataFrame contendo os dados do FIRMS.
    """

    POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")
    POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "postgres")
    POSTGRES_DATABASE = os.getenv("POSTGRES_DATABASE", "sentinela_chapada")
    POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
    POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")

    DATABASE_URL = (
        f"postgresql+psycopg2://"
        f"{POSTGRES_USER}:{POSTGRES_PASSWORD}"
        f"@{POSTGRES_HOST}:{POSTGRES_PORT}"
        f"/{POSTGRES_DATABASE}"
    )

    engine = create_engine(DATABASE_URL)

    try:
        # Testa a conexão
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))

        logging.info("Conexão com o PostgreSQL realizada com sucesso!")

        # Insere os dados
        df.to_sql(
            "firms_fire",
            con=engine,
            if_exists="append",
            index=False
        )

        logging.info(f"{len(df)} registros inseridos com sucesso!")

    except Exception as e:
        logging.error(f"Erro ao inserir dados: {e}")

    finally:
        engine.dispose()