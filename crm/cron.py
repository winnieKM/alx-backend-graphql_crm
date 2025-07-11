import os
from datetime import datetime
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

def update_low_stock():
    # GraphQL mutation string
    mutation = gql("""
    mutation {
      updateLowStockProducts {
        success
        message
        updatedProducts
      }
    }
    """)

    # Setup GraphQL client
    transport = RequestsHTTPTransport(
        url="http://localhost:8000/graphql",
        verify=False,
        retries=3,
    )

    client = Client(transport=transport, fetch_schema_from_transport=False)

    try:
        # Execute mutation
        response = client.execute(mutation)
        updated = response['updateLowStockProducts']['updatedProducts']
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        with open("/tmp/low_stock_updates_log.txt", "a") as f:
            f.write(f"{timestamp}: Updated products: {updated}\n")

        print("Low stock update completed!")

    except Exception as e:
        with open("/tmp/low_stock_updates_log.txt", "a") as f:
            f.write(f"{timestamp}: ERROR - {str(e)}\n")
        print("Error updating stock:", e)
