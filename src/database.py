import psycopg2
from collections import defaultdict
from typing import Dict, Optional
from psycopg2.extras import RealDictCursor
from urllib.parse import urlparse

connection_string = "localhost://postgres:postgres@store_monitor:5432"
p = urlparse(connection_string)

pg_connection_dict = {
    'dbname': p.hostname,
    'user': p.username,
    'password': p.password,
    'port': p.port,
    'host': p.scheme
}

con = psycopg2.connect(**pg_connection_dict)
cursor  = con.cursor(cursor_factory = RealDictCursor)



def get_store_operation_time(store_id: str) -> dict:
    cursor.execute("select day, start_time_local, end_time_local from operation_time where store_id = %s", (store_id,))
    resp = cursor.fetchall()
    operation_time = defaultdict(list)
    if resp:
        for row in resp:
            operation_time[row["day"]].append({
                "start_time_local": row["start_time_local"],
                "end_time_local": row["end_time_local"]
            })
    
    return operation_time


def get_local_timezone(store_id: str) -> Optional[str]:
    cursor.execute("select timezone from timezone_info where store_id = %s", (store_id,))
    resp = cursor.fetchone()
    return resp["timezone"] if resp else None


def get_store_statuses(store_id: str, timezone: str) -> dict:
    cursor.execute("""
    SELECT (timestamp_utc at time zone 'utc' at time zone %(timezone)s)::date as local_date,
    json_agg(json_build_object('local_timestamp',
						   (timestamp_utc at time zone 'utc' at time zone %(timezone)s)::time,
						   'status', status) order by (timestamp_utc at time zone 'utc' at time zone 'America/New_York')::time) as local_time_list
    FROM store_status where store_id = %(store_id)s
    GROUP BY (timestamp_utc at time zone 'utc' at time zone %(timezone)s)::date

    """, {"store_id": store_id, "timezone": timezone})
    resp = cursor.fetchall()
    return resp


if __name__ == "__main__":
    res = get_store_statuses("3345190510668585029", "America/New_York")
    print(res)