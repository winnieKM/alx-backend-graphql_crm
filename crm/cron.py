import os
from datetime import datetime
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

def update_low_stock():
    transport = RequestsHTTPTransport(
        url="http://localhost:8000/graphql",
        verify=True,
        retries=3,
    )

    client = Client(transport=transport, fetch_schema_from_transport=True)

    mutation = gql("""
        mutation {
            updateLowStockProducts {
                updatedProducts {
                    name
                    stock
                }
                message
            }
        }
    """)

    try:
        result = client.execute(mutation)
        updated_products = result['updateLowStockProducts']['updatedProducts']
        message = result['updateLowStockProducts']['message']

        with open("/tmp/low_stock_updates_log.txt", "a") as log_file:
            log_file.write(f"{datetime.now()}: {message}\n")
            for product in updated_products:
                log_file.write(f"  - {product['name']}: {product['stock']}\n")
    except Exception as e:
        with open("/tmp/low_stock_updates_log.txt", "a") as log_file:
            log_file.write(f"{datetime.now()}: Failed to update stock: {str(e)}\n")
