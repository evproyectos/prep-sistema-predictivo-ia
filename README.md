# prep-sistema-predictivo-ia

Repositorio de aprendizaje y preparación para el desarrollo de un sistema predictivo de calidad de agua para la ASADA La Lucha, como parte de la Práctica Profesional - UTN San Carlos 2027.

## Contexto

La ASADA La Lucha administra una red hídrica que abastece a comunidades en la zona norte de Costa Rica. Este repositorio documenta el proceso de aprendizaje previo al desarrollo del sistema de monitoreo y predicción de calidad de agua basado en sensores IoT e inteligencia artificial.

## Estructura del proyecto

```
prep-sistema-predictivo-ia/
├── mes1-python-datos/          # Python para datos, Pandas, series temporales y Docker
│   ├── eda_water_potabilit.ipynb       # EDA sobre dataset Water Potability (Kaggle)
│   ├── series_temporales.ipynb         # Series temporales, resample, rolling e interpolación
│   ├── water_potability_limpio.parquet # Dataset limpio exportado
│   └── docker-compose.yml              # PostgreSQL 15 para desarrollo local
├── mes2-machine-learning/      # Clasificación con Random Forest, SVM e Isolation Forest
│   └── clasificacion_contaminacion.ipynb  # Comparación de 3 modelos + SMOTE + Grid Search
├── mes3-deep-learning/         # LSTM, GRU, Autoencoder y MLflow
│   └── lstm_sensores_agua.ipynb        # LSTM/GRU con ventanas, Autoencoder, ONNX
├── mes4-arquitectura/          # FastAPI + Docker multi-contenedor
│   ├── api/
│   │   ├── main.py             # FastAPI app con endpoints de predicción
│   │   ├── schemas.py          # Validación Pydantic de datos de sensores
│   │   ├── predictor.py        # Lógica de carga y predicción del modelo
│   │   ├── export_modelo.py    # Script para entrenar y exportar modelo a pickle
│   │   ├── requirements-api.txt # Dependencias del contenedor API
│   │   └── Dockerfile          # Imagen Docker de la API
│   ├── tests/
│   │   └── test_api.py         # 7 tests de integración con FastAPI TestClient
│   └── docker-compose.yml      # Multi-contenedor: API + PostgreSQL + MLflow
├── src/                        # Módulos reutilizables con type hints
│   ├── data_loading.py         # Carga, exportación y conexión a PostgreSQL
│   ├── preprocessing.py        # Imputación, huecos aleatorios, interpolación
│   └── visualization.py        # Histogramas, boxplots, heatmaps, series temporales
├── tests/                      # Tests unitarios con pytest
│   └── test_preprocessing.py   # 4 tests cubriendo funciones de src/preprocessing.py
├── conftest.py                 # Configuración de pytest
├── requirements.txt            # Dependencias del proyecto (UTF-8, pip freeze)
├── .env.example                # Variables de entorno requeridas (sin credenciales reales)
├── CONTEXT.md                  # Contexto completo del proyecto para Claude Code
└── README.md
```

## Cómo correr el proyecto

### Desarrollo local (Jupyter)

```bash
git clone https://github.com/tu-usuario/prep-sistema-predictivo-ia
cd prep-sistema-predictivo-ia

python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux

pip install -r requirements.txt

cp .env.example .env
# Editá .env con tus credenciales locales

jupyter notebook
```

### Sistema completo con Docker

```bash
cd mes4-arquitectura

# Exportar modelo primero (una sola vez)
python api/export_modelo.py

# Levantar todos los servicios
docker-compose up --build
```

Servicios disponibles:
- **API de predicción:** http://localhost:8000
- **Documentación interactiva:** http://localhost:8000/docs
- **MLflow UI:** http://localhost:5001
- **PostgreSQL:** localhost:5432

### Tests

```bash
# Tests unitarios (src/)
pytest tests/ -v

# Tests de integración (API)
pytest mes4-arquitectura/tests/ -v
```

## API de predicción

### POST /predict

```json
{
  "ph": 7.2,
  "turbidez": 3.5,
  "ph_lag1": 7.1,
  "turbidez_lag1": 3.3,
  "ph_rolling3": 7.15,
  "turbidez_rolling3": 3.4
}
```

Respuesta:
```json
{
  "contaminacion_detectada": true,
  "probabilidad": 0.531,
  "modelo": "SVM + SMOTE (TimeSeriesSplit, F1=0.49)",
  "alerta": "MODERADA — posible evento de contaminación",
  "ph_recibido": 7.2,
  "turbidez_recibida": 3.5,
  "latencia_ms": 5.24
}
```

## Resultados

| Modelo | F1 clase 1 | Validación | Notas |
|---|---|---|---|
| Random Forest | 0.41 | TimeSeriesSplit 5 folds | Con SMOTE |
| **SVM** | **0.49** | TimeSeriesSplit 5 folds | **Mejor modelo — en producción** |
| Isolation Forest | 0.16 | TimeSeriesSplit 5 folds | No supervisado, sin SMOTE |
| LSTM (diario) | 0.32 | Hold-out temporal 80/20 | Ventana 7 días |
| LSTM (horario) | 0.44 | Hold-out temporal 80/20 | Ventana 24h, 2 años de datos |
| GRU | 0.31 | Hold-out temporal 80/20 | Similar a LSTM |
| Autoencoder | 77.5% detección | Umbral percentil 95 | Con anomalías estructurales |

### Latencia en producción

| Modelo | Original | ONNX Runtime |
|---|---|---|
| Random Forest | 3.29ms | 0.02ms |
| LSTM | 40.10ms | 0.03ms |
| **SVM (Docker)** | **5.24ms** | — |

Requisito ≤500ms p95: ✅ cumplido en todos los modelos

## Progreso

### Mes 1 — Python para datos ✅
- [x] Estructura del repositorio y configuración de Git
- [x] EDA sobre dataset de calidad de agua (Water Potability)
- [x] Detección e imputación de valores nulos con mediana
- [x] Pipeline CSV → limpieza → exportación a Parquet
- [x] Series temporales con DatetimeIndex, resample y rolling
- [x] Simulación de huecos aleatorios e interpolación lineal
- [x] Docker con PostgreSQL y conexión desde Python
- [x] Modularización con src/ y type hints
- [x] Tests unitarios con pytest (4 tests)

### Mes 2 — Machine Learning ✅
- [x] Comparación de Random Forest, SVM e Isolation Forest
- [x] SMOTE para desbalance de clases
- [x] Validación con TimeSeriesSplit (sin data leakage)
- [x] Etiquetas de contaminación simuladas con umbrales de pH/turbidez
- [x] Pipelines de scikit-learn + imbalanced-learn
- [x] Grid Search con scoring=F1

### Mes 3 — Deep Learning ✅
- [x] LSTM con ventanas de tiempo (7 días diario, 24h horario)
- [x] GRU comparado contra LSTM
- [x] EarlyStopping y ModelCheckpoint
- [x] Autoencoder con umbral estadístico (percentil 95)
- [x] Dataset horario mejorado (17,521 muestras, 2 años, anomalías estructurales)
- [x] Comparación de latencia: RF=3.29ms, LSTM=40.10ms
- [x] Exportación a ONNX Runtime (LSTM: 0.03ms, RF: 0.02ms)
- [x] MLflow con 8 experimentos registrados

### Mes 4 — Arquitectura ✅
- [x] FastAPI con validación Pydantic de datos de sensores
- [x] Endpoints: GET /, /health, POST /predict, GET /modelo/info
- [x] Pipeline de inferencia: StandardScaler → SVC (sin SMOTE en producción)
- [x] Dockerfile con Python 3.11-slim
- [x] Docker multi-contenedor: API + PostgreSQL + MLflow
- [x] 7 tests de integración pasando (1.91s)
- [x] Latencia en contenedor: 5.24ms (requisito ≤500ms cumplido)

## Autor

Emanuel Vargas
UTN San Carlos — Práctica Profesional 2027