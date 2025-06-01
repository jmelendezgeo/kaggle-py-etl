import os
import time
from kaggle.api.kaggle_api_extended import KaggleApi
from ingestion.models import KaggleDatasetParameters
from typing import Optional


def initialize_kaggle_api():
    """Inicializa la API de Kaggle y la autentica."""
    api = KaggleApi()
    try:
        api.authenticate()
        print("Autenticación exitosa en Kaggle.")
    except Exception as e:
        print(f"Error al autenticar Kaggle: {e}")
        return None
    return api


def download_kaggle_dataset(params: KaggleDatasetParameters) -> Optional[str]:
    """Descarga un dataset de Kaggle y mide el tiempo de ejecución."""

    api = initialize_kaggle_api()

    if not api:
        print("No se pudo autenticar la API de Kaggle. Abortando descarga.")
        return None

    os.makedirs(
        params.destination_folder, exist_ok=True
    )  # Asegurar que la carpeta existe
    start_time = time.time()

    try:
        api.dataset_download_files(
            params.dataset_name, path=params.destination_folder, unzip=True
        )
        elapsed_time = time.time() - start_time
        print(f"Descarga completada en {elapsed_time:.2f} segundos.")

        downloaded_files = os.listdir(params.destination_folder)

        if downloaded_files:
            dataset_path = os.path.join(params.destination_folder, downloaded_files[0])
            print(f"Dataset {params.dataset_name} guardado en {dataset_path}")
            return dataset_path
        return None

    except Exception as e:
        print(f"Error al descargar el dataset: {e}")
        return None
