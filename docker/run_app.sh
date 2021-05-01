#!/bin/bash
db_path="/database/database.db";
if [[ -f "$db_path" ]];
then
  touch "$db_path";
fi
uwsgi --ini ./app/production.ini;
