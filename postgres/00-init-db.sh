#!/bin/bash
set -e

echo "========================================="
echo "🔄 ЗАПУСК init-db.sh"
echo "========================================="

# Ждем PostgreSQL
echo "⏳ Ожидание запуска PostgreSQL..."
until pg_isready -U postgres; do
  sleep 2
done
echo "✅ PostgreSQL запущен"

# Проверяем файл
echo "🔍 Проверка демо-базы..."
if [ -f /tmp/demo.sql.gz ] && [ -s /tmp/demo.sql.gz ]; then
    echo "✅ Файл найден: $(du -h /tmp/demo.sql.gz | cut -f1)"

    # Простая проверка gzip (без hexdump)
    echo "📥 Проверка архива..."
    if gzip -t /tmp/demo.sql.gz 2>/dev/null; then
        echo "✅ Это валидный gzip архив"

        echo "📦 Распаковка..."
        gunzip -c /tmp/demo.sql.gz > /tmp/demo.sql 2>/dev/null

        if [ -f /tmp/demo.sql ]; then
            echo "✅ Распаковано: $(du -h /tmp/demo.sql | cut -f1)"

            echo "📊 Загрузка в PostgreSQL (это займет время)..."
            # Загружаем дамп
            if psql -U postgres -d demo -f /tmp/demo.sql 2>/tmp/load.log; then
                echo "✅ Демо-база загружена!"

                # Проверяем таблицы
                echo "📋 Проверка загруженных таблиц..."
                TABLES_COUNT=$(psql -U postgres -d demo -t -c "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = 'bookings';" 2>/dev/null || echo "0")
                echo "✅ Таблиц в схеме bookings: $TABLES_COUNT"

                # Проверяем рейсы
                FLIGHTS_COUNT=$(psql -U postgres -d demo -t -c "SELECT COUNT(*) FROM bookings.flights;" 2>/dev/null || echo "0")
                echo "✅ Рейсов в базе: $FLIGHTS_COUNT"

            else
                echo "⚠️ Ошибка загрузки"
                tail -20 /tmp/load.log
            fi
        else
            echo "❌ Не удалось распаковать"
        fi
    else
        echo "❌ Файл не является валидным gzip архивом"
    fi
else
    echo "❌ Файл демо-базы не найден или пустой"
fi

echo "========================================="
echo "✅ ИНИЦИАЛИЗАЦИЯ ЗАВЕРШЕНА"
echo "========================================="
