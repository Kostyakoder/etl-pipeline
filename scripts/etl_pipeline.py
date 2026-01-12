import pandas as pd
import psycopg2
import mysql.connector
import time

try:
    start = time.time()

    print("Подключаемся к PostgreSql")
    pg_conn = psycopg2.connect(
        host="localhost",
        port=5433,
        database="demo",
        user="postgres",
        password="simple123"
    )

    query = """
    SELECT 
        flight_id::integer,
        route_no::text,
        status::text,
        TO_CHAR(scheduled_departure, 'YYYY-MM-DD HH24:MI:SS') as scheduled_departure,
        TO_CHAR(scheduled_arrival, 'YYYY-MM-DD HH24:MI:SS') as scheduled_arrival,
        TO_CHAR(actual_departure, 'YYYY-MM-DD HH24:MI:SS') as actual_departure,
        TO_CHAR(actual_arrival, 'YYYY-MM-DD HH24:MI:SS') as actual_arrival,
        departure_airport::text,
        arrival_airport::text,
        airplane_code::text,
        departure_airport_name::text,
        departure_city::text,
        departure_country::text,
        departure_timezone::text,
        arrival_airport_name::text,
        arrival_city::text,
        arrival_country::text,
        arrival_timezone::text,
        airplane_model::text,
        airplane_range::integer,
        airplane_speed::integer,
        scheduled_duration::text,
        days_of_week::text,
        scheduled_time::text
    FROM flights_datamart
    LIMIT 30
    """

    df = pd.read_sql(query, pg_conn)
    pg_conn.close()

    print(f"   Прочитано {len(df)} строк")
    print(f"   Колонки: {list(df.columns)}")
    print(f"   Всего колонок: {len(df.columns)}")

    print("\n Подключаемся к MySQL")

    # MySQL
    mysql_conn = mysql.connector.connect(
        host="localhost",
        port=3307,
        database="etl_database",
        user="etl_user",
        password="etl_password"
    )
    cursor = mysql_conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS etl_results_full (
            id INT AUTO_INCREMENT PRIMARY KEY,
            flight_id INT,
            route_no VARCHAR(50),
            status VARCHAR(50),
            scheduled_departure VARCHAR(50),
            scheduled_arrival VARCHAR(50),
            actual_departure VARCHAR(50),
            actual_arrival VARCHAR(50),
            departure_airport VARCHAR(10),
            arrival_airport VARCHAR(10),
            airplane_code VARCHAR(10),
            departure_airport_name VARCHAR(100),
            departure_city VARCHAR(100),
            departure_country VARCHAR(100),
            departure_timezone VARCHAR(50),
            arrival_airport_name VARCHAR(100),
            arrival_city VARCHAR(100),
            arrival_country VARCHAR(100),
            arrival_timezone VARCHAR(50),
            airplane_model VARCHAR(100),
            airplane_range INT,
            airplane_speed INT,
            scheduled_duration VARCHAR(50),
            days_of_week VARCHAR(50),
            scheduled_time VARCHAR(50),
            transfer_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cursor.execute("DELETE FROM etl_results_full")

    inserted = 0
    for _, row in df.iterrows():
        try:
            cursor.execute("""
                INSERT INTO etl_results_full 
                (flight_id, route_no, status, scheduled_departure, scheduled_arrival,
                 actual_departure, actual_arrival, departure_airport, arrival_airport,
                 airplane_code, departure_airport_name, departure_city, departure_country,
                 departure_timezone, arrival_airport_name, arrival_city, arrival_country,
                 arrival_timezone, airplane_model, airplane_range, airplane_speed,
                 scheduled_duration, days_of_week, scheduled_time)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                int(row['flight_id']) if pd.notna(row['flight_id']) else None,
                str(row['route_no']) if pd.notna(row['route_no']) else '',
                str(row['status']) if pd.notna(row['status']) else '',
                str(row['scheduled_departure']) if pd.notna(row['scheduled_departure']) else None,
                str(row['scheduled_arrival']) if pd.notna(row['scheduled_arrival']) else None,
                str(row['actual_departure']) if pd.notna(row['actual_departure']) else None,
                str(row['actual_arrival']) if pd.notna(row['actual_arrival']) else None,
                str(row['departure_airport']) if pd.notna(row['departure_airport']) else '',
                str(row['arrival_airport']) if pd.notna(row['arrival_airport']) else '',
                str(row['airplane_code']) if pd.notna(row['airplane_code']) else '',
                str(row['departure_airport_name']) if pd.notna(row['departure_airport_name']) else '',
                str(row['departure_city']) if pd.notna(row['departure_city']) else '',
                str(row['departure_country']) if pd.notna(row['departure_country']) else '',
                str(row['departure_timezone']) if pd.notna(row['departure_timezone']) else '',
                str(row['arrival_airport_name']) if pd.notna(row['arrival_airport_name']) else '',
                str(row['arrival_city']) if pd.notna(row['arrival_city']) else '',
                str(row['arrival_country']) if pd.notna(row['arrival_country']) else '',
                str(row['arrival_timezone']) if pd.notna(row['arrival_timezone']) else '',
                str(row['airplane_model']) if pd.notna(row['airplane_model']) else '',
                int(row['airplane_range']) if pd.notna(row['airplane_range']) else None,
                int(row['airplane_speed']) if pd.notna(row['airplane_speed']) else None,
                str(row['scheduled_duration']) if pd.notna(row['scheduled_duration']) else '',
                str(row['days_of_week']) if pd.notna(row['days_of_week']) else '',
                str(row['scheduled_time']) if pd.notna(row['scheduled_time']) else ''
            ))
            inserted += 1
        except Exception as e:
            print(f"   Ошибка в строке {inserted}: {e}")
            continue

    mysql_conn.commit()

    cursor.execute("SELECT COUNT(*) FROM etl_results_full")
    count = cursor.fetchone()[0]

    cursor.close()
    mysql_conn.close()

    print(f"   Загружено {count} строк в MySQL")

    total_time = time.time() - start

    print(f"Результат:")
    print(f"   - Из PostgreSQL: {len(df)} строк")
    print(f"   - В MySQL: {count} строк")
    print(f"   - Колонок загружено: {len(df.columns)}")
    print(f"   - Время: {total_time:.2f} секунд")


except Exception as e:
    print(f"\n ОШИБКА: {e}")
    import traceback

    traceback.print_exc()