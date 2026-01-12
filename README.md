# ETL Pipeline: PostgreSql -> MySql

Полнофункциональный ETL pipeline для переноса данных из PostgreSql в MySql с использованием Docker, демонстрационной базы данных авиакомпаний и Python

Проект использует реальную демонстрационную базу данных авиакомпаний (https://edu.postgrespro.ru/demo-20250901-3m.sql.gz) и автоматизирует всю инфраструктуру через Docker Compose.
В ходе поднятия контейнеров базами данных возникли проблемы с портами. Поэтому для PostgreSql был установлен порт 5433 на хосте (в контейнере остался 5432), а для MySql - 3307 на хосте (в контейнере остался 3306)
После скачивания базы данных и копирования ее в контейнер с PostgreSql была создана витрина данных flights_datamart (scripts/01-create_datamart.sql). Она содержит поля из представлений базы данных и таблицы routes.
Далее был создан python-script (scripts/etl_pipeline.py), который переливает данные из витрины данных flights_datamart (postgresql) в таблицу etl_database (mysql). 

Также в чем особенность проекта. Любой желающий может установить себе репозиторий и запустить у себя, при этом не скачивая ничего дополнительного.
Это можно сделать с помощью команд:
```
# 1. Клонировать репозиторий
git clone https://github.com/Kostyakoder/etl-pipeline.git
cd etl-pipeline

# 2. Запустить инфраструктуру (первый запуск 5-10 минут)
docker compose build postgres # только для первого запуска
docker compose up -d

# 3. Дождаться инициализации демо-базы
docker compose logs -f postgres

# 4. Установить зависимости Python
cd scripts
pip install -r requirements.txt

# 5. Запустить ETL процесс
python etl_pipeline.py
```
А с помощью данных команд можно управлять Docker контейнерами:
```
# Запуск всех сервисов
docker compose up -d

# Остановка всех сервисов
docker compose down

# Просмотр логов PostgreSQL
docker compose logs -f postgres

# Просмотр логов MySQL
docker compose logs -f mysql

# Полная очистка (удаляет данные!)
docker compose down -v

# Пересборка образа PostgreSQL
docker compose build postgres
```
Эта особенность возможна благодаря docker-compose, который загружает демонстрационную базу данных авиакомпании (postgres) и поднимает контейнеры с базами данных.
