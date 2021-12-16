# curl -X 'POST' 'http://127.0.0.1:5000/name?name_of_store=test_store' -H 'accept: application/json' -d ''

# import necessary libraries
from fastapi import FastAPI
import subprocess
import os
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
import time

app = FastAPI()

# attempt to run the bash script; on failure wait 5 sec and try again, up to 5 times
tries = 5
while tries > 0:
    result = subprocess.run(["./create-database-and-tables.sh"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if result.stdout == "":
        print("Database offline, trying again shortly...")
        tries -= 1
        time.sleep(5)
    else:
        break

# if log-level is debug, print 'dev'
log_level = os.environ["LOG_LEVEL"]
mode = os.environ["MODE"]
if log_level == "debug":
    print("********** " + mode + " **********")
    
# get the login info to the db
host_server = "db"
database_name = os.environ.get("POSTGRES_DB_VAR")
db_username = os.environ.get("POSTGRES_USER_VAR")
db_password = os.environ.get("POSTGRES_PASSWORD_VAR")
SQLALCHEMY_DATABASE_URL = "postgresql://{}:{}@{}/{}".format(db_username, db_password, host_server, database_name)

# map the db to sqlalchemy
Base = automap_base()
engine = create_engine(SQLALCHEMY_DATABASE_URL)
Base.prepare(engine, reflect=True)
Store = Base.classes.store
session = Session(engine)

# by default display the bash script stdout and the log-level
@app.get("/")
def read_root():
    return {result.stdout, log_level}

# add a name provided to the db
@app.post("/name")
def name_store(name_of_store: str):
    session.add(Store(name=name_of_store))
    session.commit()
    return {name_of_store}
