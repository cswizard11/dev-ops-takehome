#!/bin/bash

# add the login info for the db
echo "db:5432:${POSTGRES_DB_VAR}:${POSTGRES_USER_VAR}:${POSTGRES_PASSWORD_VAR}" > ~/.pgpass
chmod 0600 ~/.pgpass

# login to the db and create the table
psql -h db -p 5432 -U $POSTGRES_USER_VAR $POSTGRES_DB_VAR -c "CREATE TABLE IF NOT EXISTS store( \
                                                              id SERIAL PRIMARY KEY, \
                                                              name VARCHAR NOT NULL\
                                                              );"

# remove the login info
rm ~/.pgpass
