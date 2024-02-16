import mysql.connector
from django.conf import settings

def fetch_data_from_mysql(query):
    cnx = mysql.connector.connect(
        host=(settings.HOST)[0],
        user=(settings.USER)[0],
        password=(settings.PASSWORD)[0],
        database=(settings.DB_NAME)[0]
    )

    cursor = cnx.cursor()
    cursor.execute(query)

    data = list(cursor.fetchall())
    
    cursor.close()
    cnx.close()

    return data
