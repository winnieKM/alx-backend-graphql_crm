from datetime import datetime
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport


def log_crm_heartbeat():
    now = datetime.now().strftime('%d/%m/%Y-%H:%M:%S')
    message = f"{now} CRM is alive"
    with open("/tmp/crm_heartbeat_log.txt", "a") as log_file:
        log_file.write(message + "\n")

    try:
        transport = RequestsHTTPTransport(
            url='http://localhost:8000/graphql',
            verify=True,
            retries=3,
        )
        client = Client(transport=transport, fetch_schema_from_transport=True)
        query = gql("""
        query {
            ping
        }
        """)
        client.execute(query)
    except Exception as e:
        with open("/tmp/crm_heartbeat_log.txt", "a") as log_file:
            log_file.write(f"{now} GraphQL ping failed: {str(e)}\n")


def update_low_stock():
    now = datetime.now().strftime('%d/%m/%Y-%H:%M:%S')
    try:
        transport = RequestsHTTPTransport(
            url='http://localhost:8000/graphql',
            verify=True,
            retries=3,
        )
        client = Client(transport=transport, fetch_schema_from_transport=True)

        mutation = gql("""
        mutation {
            updateLowStockProducts {
                success
                updatedProducts {
                    name
                    stock
                }
            }
        }
        """)

        result = client.execute(mutation)
        with open("/tmp/low_stock_updates_log.txt", "a") as log_file:
            log_file.write(f"{now} Stock update results:\n")
            for product in result['updateLowStockProducts']['updatedProducts']:
                log_file.write(f"- {product['name']}: {product['stock']}\n")

    except Exception as e:
        with open("/tmp/low_stock_updates_log.txt", "a") as log_file:
            log_file.write(f"{now} Failed to update stock: {str(e)}\n")
