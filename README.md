# Cloud MySQL

0. Создание инфраструктуры в папке infrastructure
   ```bash
   make tf-create-infra
   ```

   или

   ```bash
   make tf-init
   make tf-apply
   ```

1. Загрузка данных в S3
   ```bash
   make run-uploader
   ```
2. Запуск пайплайна с ML - скачаются данные, модель обучится и скрипт запишет предикты в MySQL
   ```bash
   make run-pipeline
   ```