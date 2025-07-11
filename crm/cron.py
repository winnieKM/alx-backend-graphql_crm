import datetime
import requests

def log_crm_heartbeat():
    # Timestamp in required format
    timestamp = datetime.datetime.now().strftime("%d/%m/%Y-%H:%M:%S")
    log_message = f"{timestamp} CRM is alive\n"

    # Append log to file
    with open("/tmp/crm_heartbeat_log.txt", "a") as log_file:
        log_file.write(log_message)

    # Optional: Check if GraphQL endpoint is responsive
    try:
        response = requests.post(
            "http://localhost:8000/graphql",
            json={"query": "{ hello }"},
            headers={"Content-Type": "application/json"}
        )
        if response.status_code == 200:
            print("GraphQL hello query succeeded.")
        else:
            print(f"GraphQL query failed with status code {response.status_code}")
    except Exception as e:
        print(f"GraphQL check failed: {e}")
