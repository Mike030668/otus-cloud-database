# Cloud MySQL

0. Создание инфраструктуры в папке infrastructure
   ```bash
   make tf_create_infra
   ```
1. Загрузка данных в S3 - загружаем данные в S3
   ```bash
   make run_uploader
   ```
2. Запуск пайплайна с ML - скачаются данные, модель обучится и скрипт запишет предикты в MySQL
   ```bash
   make run_pipeline
   ```