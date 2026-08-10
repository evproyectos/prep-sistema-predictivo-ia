"""
Script para exportar el modelo SVM + SMOTE entrenado en el Mes 2
al formato pickle que usa la API.

Ejecutar una sola vez desde la raíz del proyecto:
    python mes4-arquitectura/api/export_modelo.py
"""

import sys
import pickle
import numpy as np
import pandas as pd
from pathlib import Path
from sklearn.pipeline import Pipeline as SkPipeline

sys.path.append(str(Path(__file__).resolve().parent.parent.parent))

from src.data_loading import cargar_csv
from src.preprocessing import imputar_con_mediana

from imblearn.pipeline import Pipeline as ImbPipeline
from imblearn.over_sampling import SMOTE
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.model_selection import TimeSeriesSplit
from sklearn.metrics import f1_score

BASE_DIR = Path(__file__).resolve().parent.parent.parent


def entrenar_y_exportar():
    print("Cargando datos...")
    df = pd.read_parquet(BASE_DIR / "mes1-python-datos" / "water_potability_limpio.parquet")

    print("Preparando features temporales...")
    fechas = pd.date_range(start="2024-01-01", periods=len(df), freq="h")
    df.index = fechas

    df["ph_lag1"] = df["ph"].shift(1)
    df["turbidez_lag1"] = df["Turbidity"].shift(1)
    df["ph_rolling3"] = df["ph"].rolling(window=3).mean()
    df["turbidez_rolling3"] = df["Turbidity"].rolling(window=3).mean()
    df = df.dropna()

    X = df[["ph_lag1", "turbidez_lag1", "ph_rolling3", "turbidez_rolling3"]]
    y = df["Potability"]

    print("Entrenando SVM + SMOTE...")
    pipeline_entrenamiento = ImbPipeline([
        ("scaler", StandardScaler()),
        ("smote", SMOTE(random_state=42)),
        ("modelo", SVC(kernel="rbf", C=1, random_state=42, probability=True))
    ])

    pipeline_entrenamiento.fit(X, y)

    tscv = TimeSeriesSplit(n_splits=5)
    f1_scores = []
    for train_idx, test_idx in tscv.split(X):
        X_train, X_test = X.iloc[train_idx], X.iloc[test_idx]
        y_train, y_test = y.iloc[train_idx], y.iloc[test_idx]
        pipeline_val = ImbPipeline([
            ("scaler", StandardScaler()),
            ("smote", SMOTE(random_state=42)),
            ("modelo", SVC(kernel="rbf", C=1, random_state=42, probability=True))
        ])
        pipeline_val.fit(X_train, y_train)
        y_pred = pipeline_val.predict(X_test)
        f1_scores.append(f1_score(y_test, y_pred, zero_division=0))

    print(f"F1 promedio (TimeSeriesSplit): {np.mean(f1_scores):.2f}")

    print("Exportando pipeline de inferencia (sin SMOTE)...")
    pipeline_inferencia = SkPipeline([
        ("scaler", pipeline_entrenamiento.named_steps["scaler"]),
        ("modelo", pipeline_entrenamiento.named_steps["modelo"])
    ])

    output_path = Path(__file__).parent / "modelo_svm.pkl"
    with open(output_path, "wb") as f:
        pickle.dump(pipeline_inferencia, f)

    print(f"Modelo exportado en: {output_path}")
    print(f"Tamaño: {output_path.stat().st_size / 1024:.1f} KB")
    print("Pipeline de inferencia: StandardScaler → SVC (sin SMOTE)")


if __name__ == "__main__":
    entrenar_y_exportar()