import sqlite3

def insert_data(name,data_list):
    connection = sqlite3.connect('./honeyDB/honeyDB.sqlite')
    cursor = connection.cursor()
    list_length = len(data_list)
    delimiter = ','
    param_placeholder = delimiter.join('?' * len(data_list))
    insert_string = 'insert into ' + name + ' values(null,' + param_placeholder + ')'
    cursor.execute(insert_string, data_list)
    connection.commit()
    connection.close()





