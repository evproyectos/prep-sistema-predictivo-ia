"""
Funciones de preprocesamiento de datos para el proyecto
prep-sistema-predictivo-ia.
"""

import pandas as pd


def contar_nulos(df: pd.DataFrame) -> pd.Series:
    """
    Cuenta los valores nulos por columna en un DataFrame.

    Args:
        df: DataFrame a inspeccionar.

    Returns:
        Serie con el conteo de nulos por columna.
    """
    return df.isnull().sum()


def imputar_con_mediana(df: pd.DataFrame, columnas: list[str]) -> pd.DataFrame:
    """
    Imputa valores nulos en columnas específicas usando la mediana.

    Args:
        df: DataFrame original.
        columnas: Lista de nombres de columnas a imputar.

    Returns:
        Copia del DataFrame con los nulos imputados.
    """
    df_limpio = df.copy()
    for columna in columnas:
        mediana = df_limpio[columna].median()
        df_limpio[columna] = df_limpio[columna].fillna(mediana)
    return df_limpio


def inyectar_huecos_aleatorios(
    df: pd.DataFrame,
    columna: str,
    n_huecos: int,
    semilla: int = 42
) -> pd.DataFrame:
    """
    Simula fallas de sensor insertando valores nulos en posiciones aleatorias.

    Args:
        df: DataFrame con índice de tipo fecha.
        columna: Nombre de la columna donde insertar los huecos.
        n_huecos: Cantidad de valores a convertir en NaN.
        semilla: Semilla para reproducibilidad del muestreo aleatorio.

    Returns:
        Copia del DataFrame con los huecos insertados.
    """
    import numpy as np

    df_con_huecos = df.copy()
    np.random.seed(semilla)
    indices_aleatorios = np.random.choice(
        df_con_huecos.index, size=n_huecos, replace=False
    )
    df_con_huecos.loc[indices_aleatorios, columna] = np.nan
    return df_con_huecos


def interpolar_serie(df: pd.DataFrame, columna: str) -> pd.DataFrame:
    """
    Interpola linealmente los valores nulos de una columna de serie temporal.

    Args:
        df: DataFrame con índice de tipo fecha.
        columna: Nombre de la columna a interpolar.

    Returns:
        Copia del DataFrame con una columna nueva '{columna}_interpolado'.
    """
    df_resultado = df.copy()
    df_resultado[f"{columna}_interpolado"] = df_resultado[columna].interpolate(
        method="linear"
    )
    return df_resultado