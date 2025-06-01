import os
import fire
from ingestion.kaggle import download_kaggle_dataset
from ingestion.models import KaggleDatasetParameters, ProcessedDatasetParameters
from ingestion.preprocessing import normalize_columns, convert_column_types
from ingestion.loader import load_dataset_to_destination
import duckdb


def main(params: KaggleDatasetParameters):
    os.environ["KAGGLE_CONFIG_DIR"] = os.getenv(
        "KAGGLE_CONFIG_DIR", "/home/vscode/.kaggle"
    )
    raw_dataset_path = download_kaggle_dataset(params)

    if raw_dataset_path:
        print(f"Dataset descargado en: {raw_dataset_path}")
        processed_params = ProcessedDatasetParameters(
            processed_dataset_path=raw_dataset_path,
            processed_destination_folder=f"{params.destination_folder}_processed",
            **params.model_dump(),
        )

        df = normalize_columns(processed_params)
        df = convert_column_types(df, processed_params)

        config_path = os.getenv("MOTHERDUCK_CONFIG_DIR", "/home/vscode/.motherduck")

        duckdb_con = duckdb.connect()

        load_dataset_to_destination(df, processed_params, duckdb_con)

        duckdb_con.close()


if __name__ == "__main__":
    fire.Fire(lambda **kwargs: main(KaggleDatasetParameters(**kwargs)))
