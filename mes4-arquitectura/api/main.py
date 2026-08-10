"""
API de predicción de calidad de agua — ASADA La Lucha.
Sistema de alerta temprana basado en sensores IoT.
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
import time

from schemas import LecturasSensor, ResultadoPrediccion
from predictor import get_modelo, predecir


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Carga el modelo al arrancar la API."""
    try:
        get_modelo()
        print("Modelo cargado correctamente")
    except FileNotFoundError as e:
        print(f"ADVERTENCIA: {e}")
    yield


app = FastAPI(
    title="Sistema Predictivo de Calidad de Agua — ASADA La Lucha",
    description=(
        "API de predicción de eventos de contaminación en tiempo real. "
        "Recibe lecturas de sensores IoT y devuelve una predicción de "
        "contaminación con nivel de alerta."
    ),
    version="1.0.0",
    lifespan=lifespan,
)


@app.get("/")
def raiz():
    """Endpoint de bienvenida."""
    return {
        "sistema": "Sistema Predictivo de Calidad de Agua",
        "asada": "ASADA La Lucha",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health",
    }


@app.get("/health")
def health_check():
    """Verificación de estado de la API."""
    try:
        get_modelo()
        modelo_cargado = True
    except Exception:
        modelo_cargado = False

    return {
        "status": "ok" if modelo_cargado else "degradado",
        "modelo_cargado": modelo_cargado,
    }


@app.post("/predict", response_model=ResultadoPrediccion)
def predecir_contaminacion(lecturas: LecturasSensor):
    """
    Predice si hay un evento de contaminación dado un conjunto de lecturas
    de sensores IoT.

    El modelo usa las lecturas del período anterior (lag1) y el promedio
    móvil de los últimos 3 períodos (rolling3) para hacer la predicción,
    no los valores actuales directamente — esto evita data leakage.
    """
    inicio = time.perf_counter()

    try:
        resultado = predecir(
            ph=lecturas.ph,
            turbidez=lecturas.turbidez,
            ph_lag1=lecturas.ph_lag1,
            turbidez_lag1=lecturas.turbidez_lag1,
            ph_rolling3=lecturas.ph_rolling3,
            turbidez_rolling3=lecturas.turbidez_rolling3,
        )
    except FileNotFoundError as e:
        raise HTTPException(status_code=503, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en predicción: {e}")

    latencia_ms = (time.perf_counter() - inicio) * 1000
    resultado["latencia_ms"] = round(latencia_ms, 2)

    return JSONResponse(content=resultado)


@app.get("/modelo/info")
def info_modelo():
    """Información sobre el modelo en producción."""
    return {
        "nombre": "SVM + SMOTE",
        "version": "1.0.0",
        "f1_score": 0.49,
        "validacion": "TimeSeriesSplit (5 folds)",
        "features": [
            "ph_lag1",
            "turbidez_lag1",
            "ph_rolling3",
            "turbidez_rolling3"
        ],
        "umbral_decision": 0.5,
        "latencia_objetivo_ms": 500,
    }