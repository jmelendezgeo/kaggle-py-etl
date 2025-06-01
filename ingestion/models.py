from pydantic import BaseModel
from typing import Optional, List


class KaggleDatasetParameters(BaseModel):
    dataset_name: str
    destination_folder: str
    product_id_field: Optional[str] = None
    order_date_field: Optional[str] = None
    destination_loader: Optional[List[str]] = ["local"]


class ProcessedDatasetParameters(KaggleDatasetParameters):
    processed_dataset_path: str
    processed_destination_folder: str
    date_format: Optional[str] = "%d/%m/%Y"
    product_id_format: Optional[str] = "string"
    order_date_format: Optional[str] = "datetime"
    remove_duplicates: bool = True
    remove_nulls: bool = True
