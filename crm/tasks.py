from celery import shared_task
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
from datetime import datetime

@shared_task
def generate_crm_report():
    # Setup the GraphQL client
    transport = RequestsHTTPTransport(
        url="http://localhost:8000/graphql",
        verify=False,
        retries=3,
    )

    client = Client(transport=transport, fetch_schema_from_transport=True)

    # Define GraphQL query
    query = gql("""
        query {
            allCustomers {
                totalCount
            }
            allOrders {
                totalCount
                edges {
                    node {
                        totalAmount
                    }
                }
            }
        }
    """)

    try:
        result = client.execute(query)

        # Extract data
        total_customers = result['allCustomers']['totalCount']
        total_orders = result['allOrders']['totalCount']
        total_revenue = sum(
            float(order['node']['totalAmount']) for order in result['allOrders']['edges']
        )

        # Format and log the report
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_message = f"{timestamp} - Report: {total_customers} customers, {total_orders} orders, {total_revenue:.2f} revenue"

        with open("/tmp/crm_report_log.txt", "a") as f:
            f.write(log_message + "\n")

        print("CRM report generated successfully!")

    except Exception as e:
        with open("/tmp/crm_report_log.txt", "a") as f:
            f.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Error generating report: {str(e)}\n")
        print("Failed to generate CRM report")
