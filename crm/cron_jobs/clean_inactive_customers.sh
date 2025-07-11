#!/bin/bash

# Navigate to the Django project root
cd "$(dirname "$0")"

# Use full path to the virtualenv Python
DELETED_COUNT=$("/c/Users/SmallShepherd/Desktop/back end winnie kathomi/alx-backend-graphql_crm/.venv/Scripts/python.exe" manage.py shell -c "
from crm.models import Customer

inactive_customers = Customer.objects.filter(order__isnull=True)
count = inactive_customers.count()
inactive_customers.delete()
print(count)
")

# Log the result with a timestamp
echo "$(date): Deleted $DELETED_COUNT inactive customers" >> /tmp/customer_cleanup_log.txt
