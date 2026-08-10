"""
Esquemas de validación de datos para la API de predicción.
"""

from pydantic import BaseModel, Field, field_validator


class LecturasSensor(BaseModel):
    """Datos de entrada del sensor para una predicción."""

    ph: float = Field(..., ge=0.0, le=14.0, description="pH del agua (0-14)")
    turbidez: float = Field(..., ge=0.0, description="Turbidez en NTU (≥0)")
    ph_lag1: float = Field(..., description="pH del período anterior")
    turbidez_lag1: float = Field(..., description="Turbidez del período anterior")
    ph_rolling3: float = Field(..., description="Promedio móvil pH (3 períodos)")
    turbidez_rolling3: float = Field(..., description="Promedio móvil turbidez (3 períodos)")

    @field_validator("ph")
    @classmethod
    def ph_rango_realista(cls, v: float) -> float:
        if v < 4.0 or v > 11.0:
            raise ValueError(
                f"pH {v} fuera del rango realista para agua (4.0-11.0). "
                "Verificá el sensor."
            )
        return v

    @field_validator("turbidez")
    @classmethod
    def turbidez_rango_realista(cls, v: float) -> float:
        if v > 1000.0:
            raise ValueError(
                f"Turbidez {v} NTU fuera del rango realista. "
                "Verificá el sensor."
            )
        return v

    model_config = {
        "json_schema_extra": {
            "example": {
                "ph": 7.2,
                "turbidez": 3.5,
                "ph_lag1": 7.1,
                "turbidez_lag1": 3.3,
                "ph_rolling3": 7.15,
                "turbidez_rolling3": 3.4
            }
        }
    }


class ResultadoPrediccion(BaseModel):
    """Respuesta de la API con el resultado de la predicción."""

    contaminacion_detectada: bool
    probabilidad: float = Field(..., ge=0.0, le=1.0)
    modelo: str
    alerta: str
    ph_recibido: float
    turbidez_recibida: float