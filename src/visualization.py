"""
Funciones de visualización para el proyecto
prep-sistema-predictivo-ia.
"""

import matplotlib.pyplot as plt
import pandas as pd


def graficar_distribucion(
    df: pd.DataFrame, columna: str, titulo: str | None = None
) -> None:
    """
    Grafica un histograma con curva de densidad (KDE) de una columna.

    Args:
        df: DataFrame con los datos.
        columna: Nombre de la columna a graficar.
        titulo: Título opcional para la gráfica.
    """
    import seaborn as sns

    plt.figure(figsize=(8, 4))
    sns.histplot(df[columna].dropna(), bins=30, kde=True)
    plt.title(titulo or f"Distribución de {columna}")
    plt.xlabel(columna)
    plt.show()


def graficar_correlaciones(df: pd.DataFrame) -> None:
    """
    Grafica un heatmap de correlaciones entre las variables numéricas
    de un DataFrame.

    Args:
        df: DataFrame con los datos.
    """
    import seaborn as sns

    plt.figure(figsize=(10, 8))
    sns.heatmap(df.corr(), annot=True, fmt=".2f", cmap="coolwarm")
    plt.title("Correlación entre variables")
    plt.show()


def graficar_serie_con_interpolacion(
    df: pd.DataFrame,
    columna_original: str,
    columna_interpolada: str,
    titulo: str = "Interpolación de datos faltantes",
) -> None:
    """
    Grafica una serie temporal original junto a su versión interpolada.

    Args:
        df: DataFrame con índice de tipo fecha.
        columna_original: Nombre de la columna con huecos (NaN).
        columna_interpolada: Nombre de la columna ya interpolada.
        titulo: Título de la gráfica.
    """
    plt.figure(figsize=(14, 5))
    plt.plot(df.index, df[columna_original], alpha=0.4, label="Serie con huecos")
    plt.plot(df.index, df[columna_interpolada], linewidth=2, label="Serie interpolada")
    plt.title(titulo)
    plt.xlabel("Fecha")
    plt.ylabel(columna_original)
    plt.legend()
    plt.show()