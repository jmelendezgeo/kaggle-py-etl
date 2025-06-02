include .env
export

.PHONY : sales-ingest format

run:
	poetry run python -m ingestion.pipeline \
		--dataset_name $$DATASET_NAME \
		--destination_folder $$DESTINATION_FOLDER \
		--product_id_field $$PRODUCT_ID_FIELD \
		--order_date_field $$ORDER_DATE_FIELD \
		--destination_loader $$DESTINATION_LOADER 

format:
	poetry run ruff format .

test:
	poetry run pytest tests