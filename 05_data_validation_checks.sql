SELECT COUNT(*) FROM athena_db.dim_clients;
SELECT COUNT(*) FROM athena_db.dim_equipment;
SELECT COUNT(*) FROM athena_db.fact_contracts;

SELECT * FROM athena_db.dim_clients LIMIT 10;
SELECT * FROM athena_db.dim_equipment LIMIT 10;
SELECT * FROM athena_db.fact_contracts LIMIT 10;