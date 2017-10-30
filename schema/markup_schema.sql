--Creating initial tables
CREATE TABLE IF NOT EXISTS master(id INTEGER PRIMARY KEY AUTOINCREMENT, 
            key_name TEXT, score INTEGER, original_date TEXT, run_date TEXT);

CREATE TABLE IF NOT EXISTS recent(key_name TEXT PRIMARY KEY, score INTEGER);

--Query for average scores
SELECT key_name, AVG(score) FROM master GROUP BY key_name;
