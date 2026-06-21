"""
Funciones de carga y exportación de datos para el proyecto
prep-sistema-predictivo-ia.
"""

import os
import pandas as pd
from sqlalchemy import Engine, create_engine
from dotenv import load_dotenv


def cargar_csv(ruta: str) -> pd.DataFrame:
    """
    Carga un archivo CSV en un DataFrame.

    Args:
        ruta: Ruta al archivo CSV.

    Returns:
        DataFrame con los datos cargados.
    """
    return pd.read_csv(ruta)


def exportar_parquet(df: pd.DataFrame, ruta_salida: str) -> None:
    """
    Exporta un DataFrame a formato Parquet.

    Args:
        df: DataFrame a exportar.
        ruta_salida: Ruta donde se guardará el archivo .parquet.
    """
    df.to_parquet(ruta_salida, index=False)


def crear_conexion_postgres() -> Engine:
    """
    Crea un engine de SQLAlchemy para PostgreSQL usando credenciales
    definidas en variables de entorno (.env).

    Returns:
        Engine de SQLAlchemy listo para usar con pandas.to_sql() o read_sql().
    """
    os.environ["PGSYSCONFDIR"] = ""
    os.environ["PGSERVICEFILE"] = ""
    load_dotenv()

    db_user = os.getenv("DB_USER")
    db_password = os.getenv("DB_PASSWORD")
    db_host = os.getenv("DB_HOST")
    db_port = os.getenv("DB_PORT")
    db_name = os.getenv("DB_NAME")

    connection_string = (
        f"postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
    )
    return create_engine(connection_string)


def guardar_en_postgres(
    df: pd.DataFrame, nombre_tabla: str, engine: Engine
) -> None:
    """
    Guarda un DataFrame como tabla en PostgreSQL.

    Args:
        df: DataFrame a guardar.
        nombre_tabla: Nombre de la tabla destino.
        engine: Engine de SQLAlchemy ya configurado.
    """
    df.to_sql(nombre_tabla, engine, if_exists="replace", index=True)