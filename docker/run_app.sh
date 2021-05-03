#!/bin/bash
db_path="/database/database.db";
if [[ -f "$db_path" ]];
then
  touch "$db_path";
fi
echo "run tests";
python -m pytest test/ || exit 1;
echo "finish running tests";
uwsgi --ini ./app/production.ini;
