"""
Lógica de predicción para el sistema de calidad de agua.
Carga el modelo entrenado y expone una función de predicción.
"""

import os
import pickle
import numpy as np
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent


def cargar_modelo():
    """
    Carga el modelo SVM + SMOTE entrenado en el Mes 2.
    Retorna el pipeline completo (scaler + smote + modelo).
    """
    modelo_path = BASE_DIR / "modelo_svm.pkl"

    if not modelo_path.exists():
        raise FileNotFoundError(
            f"Modelo no encontrado en {modelo_path}. "
            "Ejecutá export_modelo.py primero para exportar el modelo entrenado."
        )

    with open(modelo_path, "rb") as f:
        pipeline = pickle.load(f)

    return pipeline


_modelo = None


def get_modelo():
    """Singleton — carga el modelo solo una vez al arrancar la API."""
    global _modelo
    if _modelo is None:
        _modelo = cargar_modelo()
    return _modelo


def predecir(
    ph: float,
    turbidez: float,
    ph_lag1: float,
    turbidez_lag1: float,
    ph_rolling3: float,
    turbidez_rolling3: float,
) -> dict:
    """
    Realiza una predicción de contaminación dado un conjunto de lecturas.

    Args:
        ph: pH actual del agua.
        turbidez: Turbidez actual en NTU.
        ph_lag1: pH del período anterior.
        turbidez_lag1: Turbidez del período anterior.
        ph_rolling3: Promedio móvil de pH (3 períodos).
        turbidez_rolling3: Promedio móvil de turbidez (3 períodos).

    Returns:
        Diccionario con la predicción y metadata.
    """
    modelo = get_modelo()

    features = np.array([[
        ph_lag1,
        turbidez_lag1,
        ph_rolling3,
        turbidez_rolling3
    ]])

    prediccion = modelo.predict(features)[0]
    probabilidad = modelo.predict_proba(features)[0][1]

    contaminacion = bool(prediccion == 1)

    if probabilidad >= 0.7:
        alerta = "CRÍTICA — contaminación con alta certeza"
    elif probabilidad >= 0.5:
        alerta = "MODERADA — posible evento de contaminación"
    elif probabilidad >= 0.3:
        alerta = "BAJA — monitorear de cerca"
    else:
        alerta = "NORMAL — agua dentro de parámetros"

    return {
        "contaminacion_detectada": contaminacion,
        "probabilidad": round(float(probabilidad), 4),
        "modelo": "SVM + SMOTE (TimeSeriesSplit, F1=0.49)",
        "alerta": alerta,
        "ph_recibido": ph,
        "turbidez_recibida": turbidez,
    }