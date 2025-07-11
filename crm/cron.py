import os
from datetime import datetime
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

def update_low_stock():
    mutation = gql("""
    mutation {
      updateLowStockProducts {
        success
        message
        updatedProducts
      }
    }
    """)

    transport = RequestsHTTPTransport(
        url="http://localhost:8000/graphql",
        verify=False,
        retries=3,
    )

    client = Client(transport=transport, fetch_schema_from_transport=False)

    try:
        response = client.execute(mutation)
        products = response["updateLowStockProducts"]["updatedProducts"]
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        with open("/tmp/low_stock_updates_log.txt", "a") as f:
            f.write(f"{timestamp} Updated products: {products}\n")

        print("Low stock update completed!")

    except Exception as e:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open("/tmp/low_stock_updates_log.txt", "a") as f:
            f.write(f"{timestamp} ERROR: {str(e)}\n")
