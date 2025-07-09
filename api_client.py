import requests
import time
from utils import log

# Persistent session with default headers
session = requests.Session()
session.headers.update({'Content-Type': 'application/json'})


def push_bulk_data(api_url, client_id, tables_data):
    """
    Push all tables' data in one API call to /sync/bulk/
    tables_data format:
    {
        "acc_users": [...],
        "personel": [...],
        ...
    }
    """
    log("📤 Pushing bulk data to /sync/bulk/ ...")

    if not tables_data:
        log("⚠️ No data to push")
        return False

    payload = {
        "client_id": client_id,
        "tables": tables_data
    }

    try:
        start_time = time.time()
        response = session.post(f"{api_url}/sync/bulk/", json=payload, timeout=300)

        if response.status_code in [200, 201]:
            resp_data = response.json()
            if resp_data.get("success"):
                log(f"✅ Bulk sync successful: {resp_data.get('total_processed')} records")
                return True
            else:
                log(f"❌ Bulk sync failed: {resp_data}")
                return False
        else:
            log(f"❌ Bulk sync failed - Status: {response.status_code}")
            log(f"Response: {response.text}")
            return False

    except requests.exceptions.Timeout:
        log("❌ Bulk sync request timed out after 300 seconds")
        return False
    except Exception as e:
        log(f"❌ Error during bulk sync request: {e}")
        return False
