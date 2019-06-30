#!/usr/bin/python
import psycopg2
from flask_apscheduler import APScheduler
import datetime
# from config import config

# Database credentials
hostname = 'localhost'
username = 'pankaj kumar'
password = 'quad2core'
database = 'postgres' 
 
def write_blob(vehicleType, vehicleNo, path_to_file, decision):
    """ insert a BLOB into a table """
    conn = None
    try:
        # read data from a picture
        drawing = open(path_to_file, 'rb').read()
        # read database configuration
        #params = config()
        # connect to the PostgresQL database
        conn = psycopg2.connect( host=hostname, user=username, password=password, dbname=database )
        # create a new cursor object
        cur = conn.cursor()
        # execute the INSERT statement
        cur.execute("INSERT INTO vehicleRecords(vehicleType, vehicleNo, vehicleImage, decision) VALUES(%s,%s,%s,%s)",(vehicleType, vehicleNo, psycopg2.Binary(drawing), decision))
        # commit the changes to the database
        conn.commit()
        # close the communication with the PostgresQL database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print("hi")
        print(error)
    finally:
        if conn is not None:
            conn.close()


def read_blob(vehicleNo, path_to_dir):
    """ read BLOB data from a table """
    conn = None
    try:
        # read database configuration
        #params = config()
        # connect to the PostgresQL database
        conn = psycopg2.connect( host=hostname, user=username, password=password, dbname=database )
        # create a new cursor object
        cur = conn.cursor()
        # execute the SELECT statement
        cur.execute(""" SELECT vehicleImage
                        FROM vehicleRecords
                        WHERE vehicleNo = %s """,
                    (vehicleNo,))
 
        blob = cur.fetchone()
        open(path_to_dir, 'wb').write(blob[0])
        # close the communication with the PostgresQL database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


#write_blob("e","f","images/20190629-201114.jpeg","r")

read_blob("f", "images/image.jpeg")