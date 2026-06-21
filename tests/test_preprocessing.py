"""
Tests unitarios para las funciones de src/preprocessing.py
"""


import pandas as pd
import numpy as np

from src.preprocessing import (
    contar_nulos,
    imputar_con_mediana,
    inyectar_huecos_aleatorios,
    interpolar_serie,
)


def test_contar_nulos():
    """contar_nulos() debe devolver el conteo correcto de NaN por columna."""
    df = pd.DataFrame({
        "ph": [7.0, None, 7.5, None],
        "turbidez": [3.0, 3.5, None, 4.0],
    })

    resultado = contar_nulos(df)

    assert resultado["ph"] == 2
    assert resultado["turbidez"] == 1


def test_imputar_con_mediana():
    """imputar_con_mediana() debe reemplazar todos los NaN de las
    columnas indicadas, y la mediana usada debe ser la correcta."""
    df = pd.DataFrame({
        "ph": [6.0, 7.0, None, 8.0],
    })

    resultado = imputar_con_mediana(df, columnas=["ph"])

    assert resultado["ph"].isnull().sum() == 0
    assert resultado["ph"].iloc[2] == 7.0  # mediana de [6.0, 7.0, 8.0]


def test_inyectar_huecos_aleatorios():
    """inyectar_huecos_aleatorios() debe insertar exactamente n_huecos
    valores NaN en la columna indicada."""
    fechas = pd.date_range(start="2024-01-01", periods=30, freq="D")
    df = pd.DataFrame({"ph": np.random.normal(7.2, 0.3, 30)}, index=fechas)

    resultado = inyectar_huecos_aleatorios(df, columna="ph", n_huecos=5, semilla=1)

    assert resultado["ph"].isnull().sum() == 5


def test_interpolar_serie():
    """interpolar_serie() debe rellenar los NaN de la columna interpolada
    sin dejar ningún valor nulo."""
    df = pd.DataFrame({"ph": [7.0, None, None, 7.6]})

    resultado = interpolar_serie(df, columna="ph")

    assert resultado["ph_interpolado"].isnull().sum() == 0
    assert resultado["ph_interpolado"].iloc[1] == round(7.2, 2)