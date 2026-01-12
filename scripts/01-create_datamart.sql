-- если будет ошибка, то попробуй по отдельности все запросы запустить в разных скипта

DROP TABLE IF EXISTS flights_datamart;

create table flights_datamart as
select
  t.flight_id,
  t.route_no,
  t.status,
  t.scheduled_departure,
  t.scheduled_arrival,
  t.actual_departure,
  t.actual_arrival,
  t.departure_airport,
  t.arrival_airport,
  t.airplane_code,
  dep.airport_name as departure_airport_name,
  dep.city AS departure_city,
  dep.country AS departure_country,
  dep.timezone AS departure_timezone,
  arr.airport_name AS arrival_airport_name,
  arr.city AS arrival_city,
  arr.country AS arrival_country,
  arr.timezone AS arrival_timezone,
  ap.model AS airplane_model,
  ap.range AS airplane_range,
  ap.speed AS airplane_speed,
  r.duration AS scheduled_duration,
  r.days_of_week,
  r.scheduled_time
  
from bookings.timetable t
  left join bookings.airports dep on t.departure_airport = dep.airport_code -- аэропорт вылета
  left join bookings.airports arr on t.arrival_airport = arr.airport_code -- аэропорт прибытия
  left join bookings.airplanes ap on t.airplane_code = ap.airplane_code -- самолет
  left join bookings.routes r on t.route_no = r.route_no -- маршрут

limit 30;

SELECT 'Витрина создана! Записей: ' || COUNT(*) FROM flights_datamart;