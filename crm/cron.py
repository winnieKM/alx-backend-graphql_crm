import datetime
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

def log_crm_heartbeat():
    timestamp = datetime.datetime.now().strftime("%d/%m/%Y-%H:%M:%S")
    message = f"{timestamp} CRM is alive\n"

    with open("/tmp/crm_heartbeat_log.txt", "a") as log_file:
        log_file.write(message)

    # GraphQL hello query
    transport = RequestsHTTPTransport(
        url="http://localhost:8000/graphql",
        verify=True,
        retries=3,
    )

    client = Client(transport=transport, fetch_schema_from_transport=True)

    query = gql("""
    query {
        hello
    }
    """)

    try:
        response = client.execute(query)
        print("GraphQL hello response:", response)
    except Exception as e:
        print(f"GraphQL error: {e}")
