# Second test for a method of returning JSON from a sqlite DB.
# Decided to go with this method in the code.
# NOTE: Need to run CreateTestDB first!!
# Need to manually check the output to see if it's correctly formatted into JSON.

# Code provided by StackOverflow user: Unmounted
# http://stackoverflow.com/users/11596/unmounted
# in an answer to the question "return SQL table as JSON in python"
# http://stackoverflow.com/questions/3286525/return-sql-table-as-json-in-python
# and tailored for this project's purposes

import json
import sqlite3

# Have to hardcode the database
def db(database_name='GameSeries'):
    return sqlite3.connect("GameSeries.db")

def query_db(query, args=(), one=False):
    cur = db().cursor()
    cur.execute(query, args)
    r = [dict((cur.description[i][0], value) \
               for i, value in enumerate(row)) for row in cur.fetchall()]
    cur.connection.close()
    return (r[0] if r else None) if one else r

#y = ('NES',)
#my_query = query_db("SELECT * FROM Castlevania WHERE system=?", y)
#json_output = json.dumps(my_query)
#print(json_output)

table = "Castlevania"
query_date_iso = "2008-10-22T00:00:00"
my_query = query_db("SELECT * FROM %s where (datetime > '%s')" % (table, query_date_iso))
json_output = json.dumps(my_query)
print(json_output)