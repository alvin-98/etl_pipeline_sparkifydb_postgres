import psycopg2

sever_all_connections_query = """
SELECT pg_terminate_backend(pg_stat_activity.pid)
FROM pg_stat_activity
WHERE pg_stat_activity.datname = 'sparkifydb' AND pid <> pg_backend_pid();
"""

conn = psycopg2.connect("host=127.0.0.1 dbname=studentdb user=student password=student")
conn.set_session(autocommit=True)
cur = conn.cursor()

cur.execute(sever_all_connections_query)

cur.close()
conn.close()
