#!/bin/bash

set -e 

echo "Check if database is created..."
if [ ! -f './databases/db.sqlite3' ]; then
    echo "Database is not created....[migrating]"
    python manage.py shell < ./databases/loadSemanticDatabase.py
    python manage.py migrate;
    python manage.py loaddata ./databases/fixtures/users.json;
    python manage.py loaddata ./databases/fixtures/criterias.json;
    echo "[migrated]"
fi

python manage.py runserver 0.0.0.0:10000;