# First test for a method of returning JSON from a sqlite DB.
# NOTE: Need to run CreateTestDB first!!
# Need to manually check the output to see if it's correctly formatted into JSON.

# Original code by Chad Dotson
# "Generating JSON Documents From SQLite Databases In Python"
# http://www.cdotson.com/2014/06/generating-json-documents-from-sqlite-databases-in-python/

import sqlite3

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

conn = sqlite3.connect("GameSeries.db")
conn.row_factory = dict_factory

c = conn.cursor()

c.execute("select * from Zelda")

print (c.fetchall())
conn.close()