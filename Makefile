SHELL := /bin/bash
include .env
export $(shell sed 's/=.*//' .env)

tf-init:
	terraform -chdir=infra init -upgrade

tf-plan:
	terraform -chdir=infra plan

tf-apply:
	terraform -chdir=infra apply -auto-approve

tf-destroy:
	terraform -chdir=infra destroy -auto-approve

run-pipeline:
	python3 src/main/pipeline.py

run-uploader:
	python3 src/utils/upload_data_to_s3.py

.PHONY: sync-repo
sync-repo:
	rsync -avz \
 	--exclude=.env \
 	--exclude=.venv \
 	--exclude=.git \
 	--exclude=infra/.terraform \
 	--exclude=*.tfstate \
 	--exclude=*.backup \
 	--exclude=*.json \
 	. yc-proxy:/home/ubuntu/otus/otus-cloud-database/

.PHONY: sync-env
sync-env:
	rsync -avz yc-proxy:/home/ubuntu/otus/otus-cloud-database/.env .
