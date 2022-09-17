#!/bin/bash

echo "Migrate the Database at startup of project"

# Wait for few minute and run db migraiton
while ! python3 manage.py makemigrations  2>&1; do
   echo "Make migrations are in progress "
   sleep 3
done

# Wait for few minute and run db migraiton
while ! python3 manage.py migrate  2>&1; do
   echo "Migration is in progress"
   sleep 3
done

echo "Running test before boot"

# Wait for few minute and run tests
while ! python3 manage.py test  2>&1; do
   echo "Testing is in progress"
   sleep 3
done

echo "Adding test data"

# Wait for few minute and run add users
while ! python3 manage.py users_test_data  2>&1; do
   echo "Adding users is in progress"
   sleep 3
done

# Wait for few minute and run add posts
while ! python3 manage.py posts_test_data  2>&1; do
   echo "Adding posts is in progress"
   sleep 3
done

echo "Django is fully configured successfully."

python3 manage.py runserver 0.0.0.0:8000

exec "$@"