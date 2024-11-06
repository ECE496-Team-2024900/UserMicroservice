# script to initialize the users database

import psycopg

database_url = "postgres://postgres:feF2uuFD21LHhacoQ3AB@database-capstone-user.cns26sooon4s.ca-central-1.rds.amazonaws.com:5432/postgres?sslmode=require"

connection = psycopg.connect(database_url)

cursor = connection.cursor()

cursor.execute(open("schema.sql", "r").read())

connection.commit()

cursor.close()

connection.close()