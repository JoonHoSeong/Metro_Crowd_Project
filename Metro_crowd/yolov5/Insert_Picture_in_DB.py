import mysql.connector
from PIL import Image
import base64
import io
import os

host = ''
user = ''
pw = ''
db = ''

#DB Insert
def convertToBinaryData(filename):
    # Convert digital data to binary format
    with open(filename, 'rb') as file:
        binaryData = file.read()
    return binaryData


def insertBLOB(id, photo):
    print("Inserting picture into indoor_picture table")
    try:
        connection = mysql.connector.connect(host=host,
                                             database=db,
                                             user=user,
                                             password=pw)

        cursor = connection.cursor()
        sql_insert_blob_query = """ INSERT INTO indoor_picture
                          (id, picture) VALUES (%s,%s)"""

        empPicture = convertToBinaryData(photo)
        # Convert data into tuple format
        insert_blob_tuple = (id, empPicture)
        result = cursor.execute(sql_insert_blob_query, insert_blob_tuple)
        connection.commit()
        print("Image and file inserted successfully as a BLOB into python_employee table", result)

    except mysql.connector.Error as error:
        print("Failed inserting BLOB data into MySQL table {}".format(error))

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")


root_dir = "./data/images/"
name_list = os.listdir(root_dir)
for index, name in enumerate(name_list):
    insertBLOB(index, root_dir+name)
