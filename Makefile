SHELL := /bin/bash

include .env

tf-init:
	cd infra && terraform init -upgrade

tf-plan:
	cd infra && terraform plan

tf-apply:
	cd infra && terraform apply -auto-approve

tf-destroy:
	cd infra && terraform destroy -auto-approve

tf-create-infra: tf-init tf-apply

run-pipeline:
	python3 src/main/pipeline.py

run-uploader:
	python3 src/utils/upload_data_to_s3.py

.PHONY: sync-repo
sync-repo:
	rsync -avz \
		--exclude=.venv \
		--exclude=.git \
		--exclude=infra/.terraform \
		--exclude=*.tfstate \
		--exclude=*.backup \
		--exclude=*.json . yc-proxy:/home/ubuntu/otus/otus-cloud-database

.PHONY: sync-env
sync-env:
	rsync -avz yc-proxy:/home/ubuntu/otus/otus-cloud-database/.env .env