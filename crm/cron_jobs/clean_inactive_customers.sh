#!/bin/bash

# Get current working directory of this script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR/../.." || exit 1  # Go to Django project root

# Use full path to Python from virtualenv
PYTHON="/c/Users/SmallShepherd/Desktop/back end winnie kathomi/alx-backend-graphql_crm/.venv/Scripts/python.exe"

# Run the cleanup and capture deleted count
DELETED_COUNT=$("$PYTHON" manage.py shell -c "
from crm.models import Customer

inactive_customers = Customer.objects.filter(order__isnull=True)
count = inactive_customers.count()
if count > 0:
    inactive_customers.delete()
print(count)
")

# Log to file
if [ $? -eq 0 ]; then
    echo "$(date): Deleted $DELETED_COUNT inactive customers" >> /tmp/customer_cleanup_log.txt
else
    echo "$(date): Cleanup script failed" >> /tmp/customer_cleanup_log.txt
fi
