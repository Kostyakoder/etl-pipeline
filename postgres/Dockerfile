FROM postgres:16

RUN apt-get update && apt-get install -y \
    wget \
    file \
    && rm -rf /var/lib/apt/lists/*

# Скачиваем с подробным выводом
RUN echo "Скачивание демо-базы..." && \
    wget --verbose https://edu.postgrespro.ru/demo-20250901-3m.sql.gz -O /tmp/demo.sql.gz && \
    echo "Проверка файла..." && \
    ls -lh /tmp/demo.sql.gz && \
    echo "Проверка типа файла..." && \
    file /tmp/demo.sql.gz && \
    echo "✅ Демо-база скачана"

# Копируем скрипт инициализации
COPY 00-init-db.sh /docker-entrypoint-initdb.d/
RUN chmod +x /docker-entrypoint-initdb.d/00-init-db.sh

# Настройки PostgreSQL
ENV POSTGRES_PASSWORD=simple123
ENV POSTGRES_DB=demo

# Стандартная точка входа PostgreSQL
CMD ["postgres"]
