# Pipeline de Ingesta y Preprocesamiento de Datos de Ventas

## Descripción del Proyecto

Este proyecto forma parte de mi portafolio personal. Demuestra la construcción de un pipeline de ingesta y preprocesamiento de datos robusto y reproducible. El objetivo principal es extraer un conjunto de datos de ventas de Kaggle, aplicar un preprocesamiento sencillo (limpieza de nombres de columnas, eliminación de duplicados y manejo de valores nulos), y finalmente persistir los datos limpios tanto en un archivo Parquet local como en una tabla en MotherDuck (Warehouse).

El proyecto está diseñado con buenas prácticas de desarrollo de software, incluyendo la automatización con `Makefile`, gestión de dependencias con `Poetry`, configuración mediante variables de entorno en `.env`, y scripts parametrizados.

## Características Principales

* **Extracción de Datos:** Utiliza la API de Kaggle para descargar el conjunto de datos especificado.
* **Preprocesamiento:** Aplica transformaciones básicas usando `pandas` para garantizar la calidad de los datos.
* **Almacenamiento Dual:** Persiste los datos preprocesados en un archivo Parquet local y, opcionalmente, en una tabla en MotherDuck utilizando `duckdb`.
* **Automatización:** Usa `Makefile` para orquestar la ejecución del pipeline.
* **Gestión de Dependencias:** `Poetry` asegura un entorno de desarrollo aislado y reproducible.
* **Configuración Flexible:** Variables de entorno y `Pydantic` para la validación y tipado de parámetros, permitiendo la parametrización del pipeline a través de la línea de comandos (`fire`).
* **Desarrollo en Contenedores:** Entorno de desarrollo `devcontainer` para una configuración consistente.
* **Calidad de Código:** `Ruff` para el formateo automático del código.

## Estructura del Proyecto
```console
.
├── Makefile                  # Automatización de tareas
├── README.md                 # Este archivo
├── data                      # Datos crudos descargados
│   └── train.csv
├── data_processed            # Datos preprocesados
│   └── sales_dataset.parquet
├── ingestion                 # Lógica del pipeline
│   ├── kaggle.py             # Funciones para interactuar con Kaggle
│   ├── loader.py             # Lógica para cargar datos (local y MotherDuck)
│   ├── models.py             # Modelos Pydantic para parametrización
│   ├── pipeline.py           # Orquestación del pipeline
│   └── preprocessing.py      # Funciones de preprocesamiento
├── poetry.lock               # Archivo de bloqueo de dependencias de Poetry
├── pyproject.toml            # Configuración de Poetry y dependencias
└── tests                     # Pruebas unitarias
   └── ingestion
       └── test_models.py
```

## Requisitos

* **Docker Desktop:** Necesario para el `devcontainer`.
* **Visual Studio Code:** Recomendado para una experiencia de desarrollo fluida con `devcontainers`.
* **Credenciales de Kaggle:** Un archivo `kaggle.json` con tus credenciales de API de Kaggle. Debes obtenerlo de tu perfil de Kaggle y colocarlo en la ruta especificada por la variable de entorno `KAGGLE_CONFIG_DIR`.
* **Credenciales de MotherDuck (Opcional):** Un archivo JSON con tus credenciales de MotherDuck si deseas cargar los datos allí. De lo contrario, pueden configurarse las variables para que los datos solo se guarden localmente. La ruta se especifica por `MOTHERDUCK_CREDENTIALS_FILE`.

## Configuración y Ejecución

### 1. Clonar el Repositorio

```bash
git clone git@github.com:jmelendezgeo/kaggle-py-etl.git
cd kaggle-py-etl
```

### 2. Configuración de Variables de Entorno
Crea un archivo `.env` en la raíz del proyecto con el siguiente contenido. Asegúrate de ajustar las rutas de los archivos de credenciales según tu configuración local y si estás utilizando el devcontainer.

```python
DATASET_NAME=rohitsahoo/sales-forecasting
DESTINATION_FOLDER=./data
PRODUCT_ID_FIELD=product_id
ORDER_DATE_FIELD=order_date
KAGGLE_CONFIG_DIR=/home/vscode/.kaggle # O la ruta donde tengas tu kaggle.json localmente
MOTHERDUCK_CREDENTIALS_FILE=/home/vscode/.motherduck/MotherDuck.json # O la ruta donde tengas tu MotherDuck.json localmente (opcional)
DESTINATION_LOADER=local,motherduck # Cambia a 'local' si no usas MotherDuck
DESTINATION_TABLE_NAME=sales_dataset
```

**Nota sobre rutas de credenciales en devcontainer:** Si estás utilizando el devcontainer, las rutas como `/home/vscode/.kaggle` se refieren al sistema de archivos dentro del contenedor. Asegúrate de que los archivos de credenciales se monten correctamente en el contenedor (esto se puede configurar en `devcontainer.json` si es necesario, o copiarlos manualmente una vez dentro). La forma más sencilla es crear estas carpetas y copiar los archivos dentro del contenedor una vez que se inicie. 

### 3. Iniciar el DevContainer y Preparar el Entorno
Abre el proyecto en VS Code. VS Code detectará el archivo `.devcontainer` y te preguntará si deseas reabrir en un contenedor. Acepta.

Una vez que el contenedor esté en funcionamiento, `Poetry` instalará automáticamente todas las dependencias necesarias. Esto puede tomar unos minutos la primera vez.

### 4. Preparar Archivos de Credenciales (dentro del DevContainer)
Una vez que el devcontainer esté en marcha, crea las carpetas para tus credenciales y copia los archivos JSON correspondientes:

```bash
# Para Kaggle:
mkdir -p /home/vscode/.kaggle
# Para Motherduck
mkdir -p /home/vscode/.motherduck
```

**¡Importante!** No subas kaggle.json o MotherDuck.json a tu repositorio de GitHub. Añade *.json a tu .gitignore.

### 5. Ejecutar el Pipeline
Una vez que el devcontainer esté listo y las dependencias instaladas, ejecuta el pipeline usando Makefile:

```bash
make run
```


Este comando:

Descargará el dataset de Kaggle en `./data/train.csv`.
Aplicará el preprocesamiento.
Guardará el resultado en `./data_processed/sales_dataset.parquet`.
Opcionalmente, cargará los datos en MotherDuck en la tabla `sales_dataset`.

### 6. Ejecución con Parámetros Personalizados (Opcional)
El pipeline es parametrizable a través de la línea de comandos gracias a `python-fire`. Puedes anular los valores por defecto definidos en `.env` al pasar argumentos directamente:

```bash
make run ARGS="--dataset_name another-dataset/name --destination_loader local"
```

O, directamente desde la terminal de Poetry (después de poetry shell):

```bash
poetry run python ingestion/pipeline.py --dataset_name another-dataset/name --destination_loader local
```
## Pruebas

Puedes ejecutar las pruebas unitarias para asegurar la integridad de la lógica de tu pipeline:

```bash
make test
```

## Formateo de Código

Este proyecto utiliza Ruff para asegurar un estilo de código consistente. Puedes formatear el código manualmente:
```bash
make format
```

## Contacto

Contacto
Si tienes alguna pregunta o sugerencia, no dudes en contactarme:

Jesus Melendez - https://www.linkedin.com/in/jesusmelendezgeo/ - jrmelendez.martin@gmail.com
https://github.com/jmelendezgeo