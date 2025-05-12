# Cloud MySQL

1. Создание инфраструктуры в папке infra
   ```bash
   make tf-create-infra
   ```

   или

   ```bash
   make tf-init
   make tf-apply
   ```

2. Загрузка данных в S3
   ```bash
   make run-uploader
   ```
3. Запуск пайплайна с ML - скачаются данные, модель обучится и скрипт запишет предикты в MySQL
   ```bash
   make run-pipeline
   ```