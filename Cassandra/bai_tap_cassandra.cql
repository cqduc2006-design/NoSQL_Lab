CREATE KEYSPACE IF NOT EXISTS shop
  WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 1};
USE shop;


-- 1. Tạo một bảng trả lời “10 đơn mới nhất của một khách hàng” và một bảng thứ hai cho “đơn theo ngày”.

CREATE TABLE IF NOT EXISTS orders_by_customer (
    customer_id text,
    order_ts    timestamp,
    order_id    uuid,
    total       decimal,
    status      text,
    PRIMARY KEY ((customer_id), order_ts, order_id)
) WITH CLUSTERING ORDER BY (order_ts DESC, order_id ASC);


CREATE TABLE IF NOT EXISTS orders_by_day (
    order_date  date,
    order_ts    timestamp,
    order_id    uuid,
    customer_id text,
    total       decimal,
    status      text,
    PRIMARY KEY ((order_date), order_ts, order_id)
) WITH CLUSTERING ORDER BY (order_ts DESC, order_id ASC);

BEGIN BATCH
  INSERT INTO orders_by_customer (customer_id, order_ts, order_id, total, status) VALUES ('kh-001', '2026-11-10 09:00:00', a0000000-0000-4000-8000-000000000001, 150000, 'SHIPPED');
  INSERT INTO orders_by_day (order_date, order_ts, order_id, customer_id, total, status) VALUES ('2026-11-10', '2026-11-10 09:00:00', a0000000-0000-4000-8000-000000000001, 'kh-001', 150000, 'SHIPPED');
APPLY BATCH;
BEGIN BATCH
  INSERT INTO orders_by_customer (customer_id, order_ts, order_id, total, status) VALUES ('kh-001', '2026-11-11 10:30:00', a0000000-0000-4000-8000-000000000002, 320000, 'SHIPPED');
  INSERT INTO orders_by_day (order_date, order_ts, order_id, customer_id, total, status) VALUES ('2026-11-11', '2026-11-11 10:30:00', a0000000-0000-4000-8000-000000000002, 'kh-001', 320000, 'SHIPPED');
APPLY BATCH;
BEGIN BATCH
  INSERT INTO orders_by_customer (customer_id, order_ts, order_id, total, status) VALUES ('kh-001', '2026-11-12 14:00:00', a0000000-0000-4000-8000-000000000003, 89000, 'SHIPPED');
  INSERT INTO orders_by_day (order_date, order_ts, order_id, customer_id, total, status) VALUES ('2026-11-12', '2026-11-12 14:00:00', a0000000-0000-4000-8000-000000000003, 'kh-001', 89000, 'SHIPPED');
APPLY BATCH;
BEGIN BATCH
  INSERT INTO orders_by_customer (customer_id, order_ts, order_id, total, status) VALUES ('kh-001', '2026-11-13 08:45:00', a0000000-0000-4000-8000-000000000004, 450000, 'SHIPPED');
  INSERT INTO orders_by_day (order_date, order_ts, order_id, customer_id, total, status) VALUES ('2026-11-13', '2026-11-13 08:45:00', a0000000-0000-4000-8000-000000000004, 'kh-001', 450000, 'SHIPPED');
APPLY BATCH;
BEGIN BATCH
  INSERT INTO orders_by_customer (customer_id, order_ts, order_id, total, status) VALUES ('kh-001', '2026-11-14 19:20:00', a0000000-0000-4000-8000-000000000005, 120000, 'SHIPPED');
  INSERT INTO orders_by_day (order_date, order_ts, order_id, customer_id, total, status) VALUES ('2026-11-14', '2026-11-14 19:20:00', a0000000-0000-4000-8000-000000000005, 'kh-001', 120000, 'SHIPPED');
APPLY BATCH;
BEGIN BATCH
  INSERT INTO orders_by_customer (customer_id, order_ts, order_id, total, status) VALUES ('kh-001', '2026-11-15 11:10:00', a0000000-0000-4000-8000-000000000006, 99000, 'PAID');
  INSERT INTO orders_by_day (order_date, order_ts, order_id, customer_id, total, status) VALUES ('2026-11-15', '2026-11-15 11:10:00', a0000000-0000-4000-8000-000000000006, 'kh-001', 99000, 'PAID');
APPLY BATCH;
BEGIN BATCH
  INSERT INTO orders_by_customer (customer_id, order_ts, order_id, total, status) VALUES ('kh-001', '2026-11-16 07:30:00', a0000000-0000-4000-8000-000000000007, 275000, 'PAID');
  INSERT INTO orders_by_day (order_date, order_ts, order_id, customer_id, total, status) VALUES ('2026-11-16', '2026-11-16 07:30:00', a0000000-0000-4000-8000-000000000007, 'kh-001', 275000, 'PAID');
APPLY BATCH;
BEGIN BATCH
  INSERT INTO orders_by_customer (customer_id, order_ts, order_id, total, status) VALUES ('kh-001', '2026-11-16 21:05:00', a0000000-0000-4000-8000-000000000008, 60000, 'PAID');
  INSERT INTO orders_by_day (order_date, order_ts, order_id, customer_id, total, status) VALUES ('2026-11-16', '2026-11-16 21:05:00', a0000000-0000-4000-8000-000000000008, 'kh-001', 60000, 'PAID');
APPLY BATCH;
BEGIN BATCH
  INSERT INTO orders_by_customer (customer_id, order_ts, order_id, total, status) VALUES ('kh-001', '2026-11-17 08:15:00', a0000000-0000-4000-8000-000000000009, 510000, 'PAID');
  INSERT INTO orders_by_day (order_date, order_ts, order_id, customer_id, total, status) VALUES ('2026-11-17', '2026-11-17 08:15:00', a0000000-0000-4000-8000-000000000009, 'kh-001', 510000, 'PAID');
APPLY BATCH;
BEGIN BATCH
  INSERT INTO orders_by_customer (customer_id, order_ts, order_id, total, status) VALUES ('kh-001', '2026-11-17 12:40:00', a0000000-0000-4000-8000-000000000010, 135000, 'NEW');
  INSERT INTO orders_by_day (order_date, order_ts, order_id, customer_id, total, status) VALUES ('2026-11-17', '2026-11-17 12:40:00', a0000000-0000-4000-8000-000000000010, 'kh-001', 135000, 'NEW');
APPLY BATCH;
BEGIN BATCH
  INSERT INTO orders_by_customer (customer_id, order_ts, order_id, total, status) VALUES ('kh-001', '2026-11-17 18:00:00', a0000000-0000-4000-8000-000000000011, 220000, 'NEW');
  INSERT INTO orders_by_day (order_date, order_ts, order_id, customer_id, total, status) VALUES ('2026-11-17', '2026-11-17 18:00:00', a0000000-0000-4000-8000-000000000011, 'kh-001', 220000, 'NEW');
APPLY BATCH;
BEGIN BATCH
  INSERT INTO orders_by_customer (customer_id, order_ts, order_id, total, status) VALUES ('kh-002', '2026-11-17 09:30:00', a0000000-0000-4000-8000-000000000012, 780000, 'PAID');
  INSERT INTO orders_by_day (order_date, order_ts, order_id, customer_id, total, status) VALUES ('2026-11-17', '2026-11-17 09:30:00', a0000000-0000-4000-8000-000000000012, 'kh-002', 780000, 'PAID');
APPLY BATCH;
BEGIN BATCH
  INSERT INTO orders_by_customer (customer_id, order_ts, order_id, total, status) VALUES ('kh-002', '2026-11-17 20:15:00', a0000000-0000-4000-8000-000000000013, 45000, 'NEW');
  INSERT INTO orders_by_day (order_date, order_ts, order_id, customer_id, total, status) VALUES ('2026-11-17', '2026-11-17 20:15:00', a0000000-0000-4000-8000-000000000013, 'kh-002', 45000, 'NEW');
APPLY BATCH;


SELECT order_ts, order_id, total, status
FROM orders_by_customer
WHERE customer_id = 'kh-001'
LIMIT 10;

SELECT order_ts, order_id, customer_id, total, status
FROM orders_by_day
WHERE order_date = '2026-11-17';

SELECT order_ts, order_id, customer_id, total
FROM orders_by_day
WHERE order_date = '2026-11-17' AND order_ts >= '2026-11-17 12:00:00';


-- 2. Thêm số đo cho ba cảm biến và thử một truy vấn bỏ qua partition key. Đọc thông báo lỗi.

CREATE TABLE IF NOT EXISTS readings_by_sensor (
    sensor_id   text,
    ts          timestamp,
    temperature double,
    humidity    double,
    PRIMARY KEY ((sensor_id), ts)
) WITH CLUSTERING ORDER BY (ts DESC);

INSERT INTO readings_by_sensor (sensor_id, ts, temperature, humidity) VALUES ('hn-01', '2026-10-30 08:00:00', 27.5, 71);
INSERT INTO readings_by_sensor (sensor_id, ts, temperature, humidity) VALUES ('hn-01', '2026-10-31 08:00:00', 26.9, 74);
INSERT INTO readings_by_sensor (sensor_id, ts, temperature, humidity) VALUES ('hn-01', '2026-11-01 08:00:00', 28.2, 69);
INSERT INTO readings_by_sensor (sensor_id, ts, temperature, humidity) VALUES ('hn-01', '2026-11-02 08:00:00', 28.6, 67);
INSERT INTO readings_by_sensor (sensor_id, ts, temperature, humidity) VALUES ('hn-02', '2026-10-31 08:00:00', 25.1, 80);
INSERT INTO readings_by_sensor (sensor_id, ts, temperature, humidity) VALUES ('hn-02', '2026-11-01 08:00:00', 25.8, 78);
INSERT INTO readings_by_sensor (sensor_id, ts, temperature, humidity) VALUES ('hcm-01', '2026-10-31 08:00:00', 31.2, 65);
INSERT INTO readings_by_sensor (sensor_id, ts, temperature, humidity) VALUES ('hcm-01', '2026-11-01 08:00:00', 32.0, 62);


SELECT * FROM readings_by_sensor WHERE temperature > 27;


-- 3. Đổi schema sang partition theo bucket tháng và giải thích vì sao.

CREATE TABLE IF NOT EXISTS readings_by_sensor_month (
    sensor_id   text,
    month       text, 
    ts          timestamp,
    temperature double,
    humidity    double,
    PRIMARY KEY ((sensor_id, month), ts)
) WITH CLUSTERING ORDER BY (ts DESC);

INSERT INTO readings_by_sensor_month (sensor_id, month, ts, temperature, humidity) VALUES ('hn-01', '2026-10', '2026-10-30 08:00:00', 27.5, 71);
INSERT INTO readings_by_sensor_month (sensor_id, month, ts, temperature, humidity) VALUES ('hn-01', '2026-10', '2026-10-31 08:00:00', 26.9, 74);
INSERT INTO readings_by_sensor_month (sensor_id, month, ts, temperature, humidity) VALUES ('hn-01', '2026-11', '2026-11-01 08:00:00', 28.2, 69);
INSERT INTO readings_by_sensor_month (sensor_id, month, ts, temperature, humidity) VALUES ('hn-01', '2026-11', '2026-11-02 08:00:00', 28.6, 67);
INSERT INTO readings_by_sensor_month (sensor_id, month, ts, temperature, humidity) VALUES ('hn-02', '2026-10', '2026-10-31 08:00:00', 25.1, 80);
INSERT INTO readings_by_sensor_month (sensor_id, month, ts, temperature, humidity) VALUES ('hn-02', '2026-11', '2026-11-01 08:00:00', 25.8, 78);
INSERT INTO readings_by_sensor_month (sensor_id, month, ts, temperature, humidity) VALUES ('hcm-01', '2026-10', '2026-10-31 08:00:00', 31.2, 65);
INSERT INTO readings_by_sensor_month (sensor_id, month, ts, temperature, humidity) VALUES ('hcm-01', '2026-11', '2026-11-01 08:00:00', 32.0, 62);


SELECT * FROM readings_by_sensor_month
WHERE sensor_id = 'hn-01' AND month = '2026-11' LIMIT 10;


SELECT * FROM readings_by_sensor_month
WHERE sensor_id = 'hn-01' AND month = '2026-10' AND ts >= '2026-10-31 00:00:00';


SELECT DISTINCT sensor_id, month, token(sensor_id, month) FROM readings_by_sensor_month;

