import json
from fetch_data import fetch_all_tables
from api_client import push_bulk_data
from utils import log, setup_logging

def run_sync():
    setup_logging()
    log("🚀 Starting Bulk Sync Process (Single Request for All Tables)")

    try:
        with open("config.json") as f:
            config = json.load(f)
    except Exception as e:
        log(f"❌ Error loading config.json: {e}")
        return

    dsn = config.get("dsn")
    api_url = config.get("api_url")
    client_id = config.get("client_id")

    if not all([dsn, api_url, client_id]):
        log("❌ Missing required config values (dsn, api_url, client_id)")
        return

    try:
        # Fetch all table data from DSN
        all_data = fetch_all_tables(dsn)

        if not all_data:
            log("❌ No data fetched. Exiting.")
            return

        log(f"📦 Tables fetched: {list(all_data.keys())}")

        # Push all table data in one call
        success = push_bulk_data(api_url, client_id, all_data)

        if success:
            log("✅ Bulk sync completed successfully!")
        else:
            log("❌ Bulk sync failed.")

    except Exception as e:
        log(f"🔥 Unexpected error during sync: {e}")

if __name__ == "__main__":
    run_sync()
