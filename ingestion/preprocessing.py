import pandas as pd
from ingestion.models import ProcessedDatasetParameters


def normalize_columns(params: ProcessedDatasetParameters) -> pd.DataFrame:
    """Normaliza las columnas del dataset descargado."""

    print(f"Iniciando la normalización de columnas de {params.processed_dataset_path}")

    # Cargar el dataset
    df = pd.read_csv(params.processed_dataset_path)

    # Normalizar los nombres de las columnas
    df.columns = (
        df.columns.str.strip().str.replace(" ", "_").str.replace("-", "_").str.lower()
    )

    # Renombrar las columnas según los parámetros
    df.rename(
        columns={
            params.product_id_field: "product_id",
            params.order_date_field: "order_date",
        },
        inplace=True,
    )

    # Eliminar duplicados si es necesario
    if params.remove_duplicates:
        print("Eliminando filas duplicadas...")
        df.drop_duplicates(inplace=True)

    # Eliminar filas con valores nulos si es necesario
    if params.remove_nulls:
        print("Eliminando filas con valores nulos...")
        df.dropna(inplace=True)

    return df


def convert_column_types(
    df: pd.DataFrame, params: ProcessedDatasetParameters
) -> pd.DataFrame:
    """Convierte los tipos de columnas según los parámetros."""

    type_mapping = {
        "string": str,
        "int": int,
    }

    print("Iniciando la conversión de tipos de columnas...")

    if params.product_id_format in type_mapping:
        df["product_id"] = df["product_id"].astype(
            type_mapping[params.product_id_format]
        )

    if params.order_date_format:
        df["order_date"] = pd.to_datetime(
            df["order_date"], format=params.date_format, errors="coerce"
        )

    return df
