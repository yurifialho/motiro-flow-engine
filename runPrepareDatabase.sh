#!/bin/bash

set -e 

python manage.py shell < ./databases/loadSemanticDatabase.py
python manage.py migrate;
python manage.py loaddata ./databases/fixtures/users.json;
python manage.py loaddata ./databases/fixtures/criterias.json;
echo "[migrated]"
