"""
Tests de integración para la API de predicción de calidad de agua.
"""

import pytest
from fastapi.testclient import TestClient
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent / "api"))

from main import app

client = TestClient(app)


def test_raiz():
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "sistema" in data
    assert "version" in data


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "modelo_cargado" in data


def test_predict_agua_normal():
    response = client.post("/predict", json={
        "ph": 7.2,
        "turbidez": 3.5,
        "ph_lag1": 7.1,
        "turbidez_lag1": 3.3,
        "ph_rolling3": 7.15,
        "turbidez_rolling3": 3.4
    })
    assert response.status_code == 200
    data = response.json()
    assert "contaminacion_detectada" in data
    assert "probabilidad" in data
    assert "alerta" in data
    assert 0.0 <= data["probabilidad"] <= 1.0


def test_predict_ph_invalido():
    response = client.post("/predict", json={
        "ph": 0.5,
        "turbidez": 3.5,
        "ph_lag1": 7.1,
        "turbidez_lag1": 3.3,
        "ph_rolling3": 7.15,
        "turbidez_rolling3": 3.4
    })
    assert response.status_code == 422


def test_predict_turbidez_invalida():
    response = client.post("/predict", json={
        "ph": 7.2,
        "turbidez": 9999.0,
        "ph_lag1": 7.1,
        "turbidez_lag1": 3.3,
        "ph_rolling3": 7.15,
        "turbidez_rolling3": 3.4
    })
    assert response.status_code == 422


def test_predict_contaminacion_alta():
    response = client.post("/predict", json={
        "ph": 5.0,
        "turbidez": 8.0,
        "ph_lag1": 5.1,
        "turbidez_lag1": 9.0,
        "ph_rolling3": 5.2,
        "turbidez_rolling3": 8.5
    })
    assert response.status_code == 200
    data = response.json()
    assert "probabilidad" in data


def test_modelo_info():
    response = client.get("/modelo/info")
    assert response.status_code == 200
    data = response.json()
    assert data["f1_score"] == 0.49
    assert "features" in data