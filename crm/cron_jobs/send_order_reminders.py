#!/usr/bin/env python3

import datetime
import logging
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

# Setup logging
LOG_FILE = "/tmp/order_reminders_log.txt"
logging.basicConfig(filename=LOG_FILE, level=logging.INFO)

# Timestamp
now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# GraphQL transport
transport = RequestsHTTPTransport(
    url="http://localhost:8000/graphql",
    verify=True,
    retries=3,
)

client = Client(transport=transport, fetch_schema_from_transport=True)

# Date range for last 7 days
today = datetime.date.today()
seven_days_ago = today - datetime.timedelta(days=7)

# GraphQL query
query = gql(
    """
    query GetRecentOrders($startDate: Date!) {
        orders(orderDate_Gte: $startDate) {
            id
            customer {
                email
            }
        }
    }
    """
)

variables = {
    "startDate": seven_days_ago.isoformat()
}

try:
    response = client.execute(query, variable_values=variables)
    orders = response.get("orders", [])

    if not orders:
        logging.info(f"{now} - No recent orders found.")
    else:
        for order in orders:
            order_id = order.get("id")
            customer_email = order.get("customer", {}).get("email", "N/A")
            logging.info(f"{now} - Order #{order_id} → {customer_email}")
except Exception as e:
    logging.error(f"{now} - Error querying orders: {str(e)}")

print("Order reminders processed!")
