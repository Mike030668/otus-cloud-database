# main.tf Основной файл конфигурации Terraform

# Создание сети и подсети

resource "yandex_vpc_network" "network" {
  name = var.yc_network_name
}

resource "yandex_vpc_subnet" "subnet" {
  zone           = var.yc_zone
  network_id     = yandex_vpc_network.network.id
  v4_cidr_blocks = [var.yc_subnet_range]
}

################################################################################

# Создание сервисного аккаунта
resource "yandex_iam_service_account" "sa" {
  name        = var.yc_service_account_name
  description = "Service account for Dataproc cluster and related services"
}

# Назначение ролей сервисному аккаунту
resource "yandex_resourcemanager_folder_iam_member" "sa_roles" {
  for_each = toset([
    "storage.admin",
    "storage.uploader",
    "storage.viewer",
    "storage.editor"
  ])
  
  folder_id = var.yc_folder_id
  role      = each.key
  member    = "serviceAccount:${yandex_iam_service_account.sa.id}"
}

################################################################################

# Создание статического ключа доступа для сервисного аккаунта
resource "yandex_iam_service_account_static_access_key" "sa-static-key" {
  service_account_id = yandex_iam_service_account.sa.id
}

# Запись ключей в .env и sa-keys.json
resource "null_resource" "update_env_and_save_keys" {
  provisioner "local-exec" {
    command = <<EOT
      # Определяем переменные для access_key и secret_key
      ACCESS_KEY=${yandex_iam_service_account_static_access_key.sa-static-key.access_key}
      SECRET_KEY=${yandex_iam_service_account_static_access_key.sa-static-key.secret_key}

      # Замена пустых переменных в .env
      sed -i "s/^S3_ACCESS_KEY=.*/S3_ACCESS_KEY=$ACCESS_KEY/" ../.env
      sed -i "s/^S3_SECRET_KEY=.*/S3_SECRET_KEY=$SECRET_KEY/" ../.env
    EOT
  }

  # Добавляем зависимости, чтобы эта команда выполнялась после создания ключей
  depends_on = [
    yandex_iam_service_account_static_access_key.sa-static-key
  ]
}

################################################################################

# Создание бакета

resource "random_id" "bucket_id" {
  byte_length = 8
}

resource "yandex_storage_bucket" "bucket" {
  bucket        = "${var.yc_bucket_name}-${random_id.bucket_id.hex}"
  access_key    = yandex_iam_service_account_static_access_key.sa-static-key.access_key
  secret_key    = yandex_iam_service_account_static_access_key.sa-static-key.secret_key
  force_destroy = true
}

resource "null_resource" "update_env_and_save_bucket_name" {
  provisioner "local-exec" {
    command = <<EOT
      # Определяем переменную BUCKET_NAME с именем бакета
      BUCKET_NAME=${yandex_storage_bucket.bucket.bucket}

      # Замена переменной BUCKET_NAME в .env
      sed -i "s/^S3_BUCKET_NAME=.*/S3_BUCKET_NAME=$BUCKET_NAME/" ../.env
    EOT
  }

  # Добавляем зависимости, чтобы эта команда выполнялась после создания ключей
  depends_on = [
    yandex_storage_bucket.bucket
  ]
}

################################################################################

# MySQL ресурсы
resource "yandex_mdb_mysql_cluster" "cluster" {
  name        = var.yc_mysql_cluster_name
  environment = var.yc_mysql_environment
  network_id  = yandex_vpc_network.network.id
  version     = var.yc_mysql_version

resources {
    resource_preset_id = var.mysql_resource_preset_id
    disk_type_id       = var.mysql_disk_type_id
    disk_size          = var.mysql_disk_size
  }

  mysql_config = var.mysql_config

  host {
    zone      = var.yc_zone
    subnet_id = yandex_vpc_subnet.subnet.id
    assign_public_ip = true
  }
}

resource "yandex_mdb_mysql_database" "db" {
  cluster_id = yandex_mdb_mysql_cluster.cluster.id
  name       = var.mysql_database_name
}

resource "yandex_mdb_mysql_user" "user" {
  cluster_id = yandex_mdb_mysql_cluster.cluster.id
  name       = var.mysql_user_name
  password   = var.mysql_user_password

  permission {
    database_name = yandex_mdb_mysql_database.db.name
    roles         = ["ALL"]
  }
}

resource "null_resource" "update_env_with_db_host" {
  provisioner "local-exec" {
    command = <<EOT
      # Определяем переменную DB_HOST с FQDN кластера
      DB_HOST=${yandex_mdb_mysql_cluster.cluster.host[0].fqdn}

      # Замена переменной DB_HOST в .env
      sed -i "s/^DB_HOST=.*/DB_HOST=$DB_HOST/" ../.env
    EOT
  }

  # Указываем, что выполнение этого провиженера зависит от успешного создания кластера
  depends_on = [
    yandex_mdb_mysql_cluster.cluster
  ]
}

# Установка порта MySQL в .env
resource "null_resource" "update_env_with_db_port" {
  depends_on = [yandex_mdb_mysql_cluster.cluster]

  provisioner "local-exec" {
    command = <<EOT
      # Удаляем старую строку с DB_PORT, если она есть
      sed -i '/^DB_PORT=/d' ../.env

      # Добавляем новую строку с портом
      echo "DB_PORT=3306" >> ../.env
    EOT
  }
}


resource "null_resource" "update_env_with_db_user" {
  depends_on = [yandex_mdb_mysql_user.user]

  provisioner "local-exec" {
    command = <<EOT
      # Определяем переменную DB_USER из имени пользователя базы данных
      DB_USER=${yandex_mdb_mysql_user.user.name}

      # Замена переменной DB_USER в .env
      sed -i "s/^DB_USER=.*/DB_USER=$DB_USER/" ../.env
    EOT
  }
}

resource "null_resource" "update_env_with_db_password" {
  depends_on = [yandex_mdb_mysql_user.user]

  provisioner "local-exec" {
    command = <<EOT
      # Удаляем старую строку с DB_PASSWORD, если она есть
      sed -i '/^DB_PASSWORD=/d' ../.env

      # Добавляем новую строку с паролем
      echo "DB_PASSWORD=${yandex_mdb_mysql_user.user.password}" >> ../.env
    EOT
  }
}



resource "null_resource" "update_env_with_db_name" {
  depends_on = [yandex_mdb_mysql_database.db]

  provisioner "local-exec" {
    command = <<EOT
      # Определяем переменную DB_NAME из имени базы данных
      DB_NAME=${yandex_mdb_mysql_database.db.name}

      # Замена переменной DB_NAME в .env
      sed -i "s/^DB_NAME=.*/DB_NAME=$DB_NAME/" ../.env
    EOT
  }
}


resource "null_resource" "update_env_with_ssl_path" {
  provisioner "local-exec" {
    command = <<EOT
      # Удаляем старую строку с SSL_PATH
      sed -i '/^SSL_PATH=/d' ../.env

      # Добавляем новый путь (пример пути)
      echo "SSL_PATH=/home/mike030668/study_projects/OTUS_MLOPS_CODE/otus-cloud-database/certs/ca.pem" >> ../.env
    EOT
  }
}
