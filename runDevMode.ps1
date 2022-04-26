
Write-Output "Check if database is created..."
if (-not(Test-Path -Path './databases/db.sqlite3' -PathType Leaf)) {
    Write-Output "Database is not created....[migrating]"
    python manage.py shell --command="exec(open('databases/loadSemanticDatabase.py').read())"
    python manage.py migrate;
    python manage.py loaddata ./databases/fixtures/users.json;
    python manage.py loaddata ./databases/fixtures/criterias.json;
    Write-Output "[migrated]"
}

python manage.py runserver 0.0.0.0:10000;