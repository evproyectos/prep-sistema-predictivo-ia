# prep-sistema-predictivo-ia

Repositorio de aprendizaje y preparación para el desarrollo de un sistema predictivo de calidad de agua para la ASADA La Lucha, como parte de la Práctica Profesional - UTN San Carlos 2027.

## Contexto

La ASADA La Lucha administra una red hídrica que abastece a comunidades en la zona norte de Costa Rica. Este repositorio documenta el proceso de aprendizaje previo al desarrollo del sistema de monitoreo y predicción de calidad de agua basado en sensores IoT e inteligencia artificial.

## Estructura del proyecto

```
prep-sistema-predictivo-ia/
├── mes1-python-datos/          # Python para datos, Pandas, series temporales y Docker
│   ├── eda_water_potability.ipynb      # Análisis exploratorio de datos
│   ├── series_temporales.ipynb         # Series temporales, resample, rolling e interpolación
│   ├── water_potability_limpio.parquet # Dataset limpio exportado
│   └── docker-compose.yml              # PostgreSQL 15 para desarrollo local
├── mes2-machine-learning/      # Próximamente
├── mes3-deep-learning/         # Próximamente
├── mes4-arquitectura/          # Próximamente
├── requirements.txt            # Dependencias del proyecto
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

### 4. Levantar la base de datos
```bash
cd mes1-python-datos
docker-compose up -d
```

### 5. Abrir Jupyter
```bash
jupyter notebook
```

## Progreso

### Mes 1 — Python para datos
- [x] Estructura del repositorio y configuración de Git
- [x] EDA sobre dataset de calidad de agua (Water Potability)
- [x] Detección e imputación de valores nulos con mediana
- [x] Pipeline CSV → limpieza → exportación a Parquet
- [x] Series temporales con DatetimeIndex, resample y rolling
- [x] Simulación de huecos en datos e interpolación lineal
- [x] Docker con PostgreSQL y conexión desde Python

### Mes 2 — Machine Learning
- [ ] Próximamente

### Mes 3 — Deep Learning
- [ ] Próximamente

### Mes 4 — Arquitectura
- [ ] Próximamente

## Autor

Emanuel Vargas
UTN San Carlos — Práctica Profesional 2027