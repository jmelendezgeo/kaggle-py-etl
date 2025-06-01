import duckdb
import os
import pandas as pd
import json


def load_motherduck_token() -> str:
    creds_path = os.getenv(
        "MOTHERDUCK_CREDENTIALS_FILE", "/home/vscode/.motherduck/MotherDuck.json"
    )

    try:
        with open(creds_path, "r") as f:
            creds = json.load(f)
            return creds.get("token", None)
    except FileNotFoundError:
        raise ValueError("No se encontró el archivo de credenciales de MotherDuck.")
    except json.JSONDecodeError:
        raise ValueError("Error al leer el archivo JSON de credenciales.")


def load_dataset_to_parquet(df, params, duckdb_con, table_name) -> str:
    """Guarda el DataFrame como Parquet utilizando DuckDB dentro de processed_destination_folder."""

    # Asegurar que la carpeta de destino exista
    os.makedirs(params.processed_destination_folder, exist_ok=True)

    print(
        f"Iniciando la carga del dataset a Parquet en {params.processed_destination_folder}"
    )
    # Definir el path completo del archivo Parquet
    parquet_path = os.path.join(
        params.processed_destination_folder, f"{table_name}.parquet"
    )
    # Usar DuckDB para guardar el DataFrame en formato Parquet
    con = duckdb_con
    con.execute(f"COPY (SELECT * FROM df) TO '{parquet_path}' (FORMAT 'parquet');")

    print(f"Dataset guardado en: {parquet_path}")


def load_dataset_to_destination(
    df: pd.DataFrame, params, duckdb_con: duckdb.DuckDBPyConnection
) -> str:
    """Carga el DataFrame a la base de datos DuckDB en MotherDuck."""

    table_name = "sales_dataset"

    if "local" in params.destination_loader:
        # Guardar el DataFrame como Parquet localmente

        load_dataset_to_parquet(df, params, duckdb_con, table_name)

    if "motherduck" in params.destination_loader:
        # Conectar a MotherDuck
        token = load_motherduck_token()
        motherduck_con = duckdb.connect(f"md:?token={token}")

        motherduck_con.execute(
            f"CREATE TABLE IF NOT EXISTS {table_name} AS SELECT * FROM df"
        )
        print("Tabla cargada en MotherDuck.")
