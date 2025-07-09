import pyodbc
import time
from utils import log
from table_mapping import TABLE_MAPPING
from decimal import Decimal

def safe_convert(value):
    if isinstance(value, Decimal):
        return float(value)
    return value

def connect_with_retry(dsn, retries=3, delay=5):
    for attempt in range(retries):
        try:
            log(f"🔌 Attempting connection to DSN '{dsn}' (try {attempt + 1})...")
            conn = pyodbc.connect(
                f"DSN={dsn};ConnectionTimeout=30",
                autocommit=True
            )
            log(f"✅ Connected to DSN '{dsn}' successfully.")
            return conn
        except pyodbc.Error as e:
            log(f"⚠️ Connection attempt {attempt + 1} failed: {e}")
            if attempt < retries - 1:
                log(f"⏳ Retrying in {delay} seconds...")
                time.sleep(delay)
            else:
                raise

def fetch_all_tables(dsn, batch_size=2000):
    results = {}

    try:
        conn = connect_with_retry(dsn)
        cursor = conn.cursor()

        for table_key, config in TABLE_MAPPING.items():
            table = config['table']
            columns = config.get('columns', '*')
            condition = config.get('condition')

            query = f"SELECT {columns} FROM {table}"
            if condition:
                query += f" WHERE {condition}"

            log(f"🔍 Querying [{table_key}]: {query}")
            try:
                cursor.execute(query)
                column_names = [col[0] for col in cursor.description]
                data = []

                try:
                    all_rows = cursor.fetchall()
                    for row in all_rows:
                        record = {col: safe_convert(val) for col, val in zip(column_names, row)}
                        data.append(record)
                    log(f"✅ {table_key}: fetched {len(data)} rows")
                except:
                    # Batch fallback
                    batch_num = 1
                    while True:
                        rows = cursor.fetchmany(batch_size)
                        if not rows:
                            break
                        for row in rows:
                            record = {col: safe_convert(val) for col, val in zip(column_names, row)}
                            data.append(record)
                        log(f"📦 {table_key} - Batch {batch_num} fetched: {len(rows)} records")
                        batch_num += 1

                results[table_key] = data

            except Exception as e:
                log(f"❌ Failed to fetch {table_key}: {e}")
                results[table_key] = None

        conn.close()
    except Exception as e:
        log(f"❌ Could not complete fetch_all_tables: {e}")
        return None

    return results
