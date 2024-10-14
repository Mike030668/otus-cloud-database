SHELL := /bin/bash

include .env

tf_init:
	cd infrastructure && terraform init -upgrade

tf_plan:
	cd infrastructure && terraform plan

tf_apply:
	cd infrastructure && terraform apply -auto-approve

tf_destroy:
	cd infrastructure && terraform destroy -auto-approve

tf_create_infra: tf_init tf_apply

run_pipeline:
	python3 src/main/pipeline.py

run_uploader:
	python3 src/utils/upload_data_to_s3.py