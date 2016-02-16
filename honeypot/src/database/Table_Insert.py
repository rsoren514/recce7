import sqlite3
from honeypot.src.database import DB_Init

'''this method will have to change somewhat. The group decided they wanted the plugin
   writers to populate a dictionary instead of a list that maps the name (column) to the
   value to be inserted that way they do not have to worry about order when calling this
   function'''


def insert_data(name, data_list):
    connection = sqlite3.connect(DB_Init.get_home_dir() + DB_Init.get_home_config_path() + '/' +
                                 DB_Init.get_database_config_name())
    cursor = connection.cursor()
    delimiter = ','
    param_placeholder = delimiter.join('?' * len(data_list))
    insert_string = 'insert into ' + name + ' values(null,' + param_placeholder + ')'
    cursor.execute(insert_string, data_list)
    connection.commit()
    connection.close()





