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
├── mes4-arquitectura/          # Próximamente
├── src/                        # Módulos reutilizables con type hints
│   ├── data_loading.py         # Carga, exportación y conexión a PostgreSQL
│   ├── preprocessing.py        # Imputación, huecos aleatorios, interpolación
│   └── visualization.py        # Histogramas, boxplots, heatmaps, series temporales
├── tests/                      # Tests unitarios con pytest
│   └── test_preprocessing.py   # 4 tests cubriendo funciones de src/preprocessing.py
├── requirements.txt            # Dependencias del proyecto (UTF-8, pip freeze)
├── .env.example                # Variables de entorno requeridas (sin credenciales reales)
└── README.md
```

## Cómo correr el proyecto

### 1. Clonar el repositorio
```bash
git clone https://github.com/tu-usuario/prep-sistema-predictivo-ia
cd prep-sistema-predictivo-ia
```

### 2. Crear el ambiente virtual
```bash
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno
```bash
cp .env.example .env
# Editá .env con tus credenciales locales
```

### 5. Levantar la base de datos
```bash
cd mes1-python-datos
docker-compose up -d
```

### 6. Abrir Jupyter
```bash
jupyter notebook
```

### 7. Correr los tests
```bash
pytest tests/ -v
```

## Resultados

| Modelo | F1 clase 1 | Validación | Notas |
|---|---|---|---|
| Random Forest | 0.41 | TimeSeriesSplit 5 folds | Con SMOTE |
| SVM | 0.49 | TimeSeriesSplit 5 folds | Con SMOTE — mejor modelo |
| Isolation Forest | 0.16 | TimeSeriesSplit 5 folds | No supervisado, sin SMOTE |
| LSTM | 0.32 | Hold-out temporal 80/20 | Ventana 7 días, class_weight |
| GRU | 0.31 | Hold-out temporal 80/20 | Ventana 7 días, class_weight |
| Autoencoder | 0/43 detectados | Umbral μ+2σ | Falla con anomalías marginales |

**Conclusión:** SVM + SMOTE es el mejor modelo con datos limitados (F1=0.49). LSTM y GRU necesitan más volumen de datos para superar los modelos clásicos. El Autoencoder requiere anomalías estructuralmente distintas para funcionar correctamente.

## Progreso

### Mes 1 — Python para datos
- [x] Estructura del repositorio y configuración de Git
- [x] EDA sobre dataset de calidad de agua (Water Potability)
- [x] Detección e imputación de valores nulos con mediana
- [x] Pipeline CSV → limpieza → exportación a Parquet
- [x] Series temporales con DatetimeIndex, resample y rolling
- [x] Simulación de huecos aleatorios e interpolación lineal
- [x] Docker con PostgreSQL y conexión desde Python
- [x] Modularización con src/ y type hints
- [x] Tests unitarios con pytest (4 tests)

### Mes 2 — Machine Learning
- [x] Comparación de Random Forest, SVM e Isolation Forest
- [x] SMOTE para desbalance de clases
- [x] Validación con TimeSeriesSplit (sin data leakage)
- [x] Etiquetas de contaminación simuladas con umbrales de pH/turbidez
- [x] Pipelines de scikit-learn + imbalanced-learn
- [x] Grid Search con scoring=F1

### Mes 3 — Deep Learning
- [x] LSTM con ventanas de tiempo (7 días)
- [x] GRU comparado contra LSTM
- [x] EarlyStopping y ModelCheckpoint
- [x] Autoencoder con umbral estadístico documentado
- [x] Comparación de latencia: RF=3.29ms, LSTM=40.10ms
- [x] Exportación a ONNX Runtime (LSTM: 0.03ms, RF: 0.02ms)
- [x] MLflow con 6 experimentos registrados

### Mes 4 — Arquitectura
- [ ] Próximamente

## Autor

Emanuel Vargas
UTN San Carlos — Práctica Profesional 2027