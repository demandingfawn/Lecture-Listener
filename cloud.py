import mysql.connector
import logging
import boto3
from botocore.exceptions import ClientError

def upload_file(file_name, object_name=None):

    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = file_name

    # Upload the file
    s3_client = boto3.client('s3')
    try:
        response = s3_client.upload_file(file_name, 'lecturelistener', object_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True


def download_file(object_name,file_name):
    s3 = boto3.client('s3')
    s3.download_file('lecturelistener',object_name,file_name)


def add_user(user_id):

    mydb = mysql.connector.connect(
        host="lecture-listener-database.ced4pprbqpl5.us-east-2.rds.amazonaws.com",
        user="admin",
        password="CS4366Group"
    )

    mycursor = mydb.cursor()
    sql = "INSERT INTO user (user_id,font_size,font_type,font_color,background_color) VALUES (%s,%s,%s,%s,%s)"
    val = (user_id,"12","Calabri","White","Black")
    mycursor.execute(sql, val)

    mydb.commit()


def add_lecture(user_id,lecture_id,date,length,course,audio,transcript):

    mydb = mysql.connector.connect(
        host = "lecture-listener-database.ced4pprbqpl5.us-east-2.rds.amazonaws.com",
        user = "admin",
        password = "CS4366Group"
    )

    mycursor = mydb.cursor()
    sql = "INSERT INTO users (user_id,lecture_id,date,length,course,audio,transcript) VALUES (%s,%s,%s,%s,%s,%s,%s)"
    val = (user_id,lecture_id,date,length,course,audio,transcript)
    mycursor.execute(sql, val)

    mydb.commit()


def add_timestamp(lecture_id,time):

    mydb = mysql.connector.connect(
        host = "lecture-listener-database.ced4pprbqpl5.us-east-2.rds.amazonaws.com",
        user = "admin",
        password = "CS4366Group"
    )

    mycursor = mydb.cursor()
    sql = "INSERT INTO users (lecture_id,time) VALUES (%s,%s)"
    val = (lecture_id,time)
    mycursor.execute(sql, val)

    mydb.commit()


def update_settings(user_id, font_size, font_type, font_color, background_color):

    mydb = mysql.connector.connect(
        host="lecture-listener-database.ced4pprbqpl5.us-east-2.rds.amazonaws.com",
        user="admin",
        password="CS4366Group"
    )

    mycursor = mydb.cursor()
    if (font_size != "NULL"):
        sql = "UPDATE customers SET font_size = %s WHERE user_id = %s"
        val = (font_size, user_id)
        mycursor.execute(sql, val)
    if (font_type != "NULL"):
        sql = "UPDATE customers SET font_type = %s WHERE user_id = %s"
        val = (font_type, user_id)
        mycursor.execute(sql, val)
    if (font_color != "NULL"):
        sql = "UPDATE customers SET font_color = %s WHERE user_id = %s"
        val = (font_color, user_id)
        mycursor.execute(sql, val)
    if (background_color != "NULL"):
        sql = "UPDATE customers SET background_color = %s WHERE user_id = %s"
        val = (background_color, user_id)
        mycursor.execute(sql, val)

    mydb.commit()


def update_settings(user_id,lecture_id,course):

    mydb = mysql.connector.connect(
        host="lecture-listener-database.ced4pprbqpl5.us-east-2.rds.amazonaws.com",
        user="admin",
        password="CS4366Group"
    )

    mycursor = mydb.cursor()
    sql = "UPDATE customers SET course = %s WHERE user_id = %s AND lecture_id = %s"
    val = (course,user_id,lecture_id)
    mycursor.execute(sql, val)

    mydb.commit()


def delete_lecture(user_id,lecture_id):

    mydb = mysql.connector.connect(
        host="lecture-listener-database.ced4pprbqpl5.us-east-2.rds.amazonaws.com",
        user="admin",
        password="CS4366Group",
        database="lecture-listener-database"
    )

    mycursor = mydb.cursor()
    sql = "DELETE FROM lecture WHERE user_id = %s AND lecture_id = %s"
    val = (user_id,lecture_id)
    mycursor.execute(sql, val)

    mydb.commit()


def delete_timestamp(lecture_id):

    mydb = mysql.connector.connect(
        host="lecture-listener-database.ced4pprbqpl5.us-east-2.rds.amazonaws.com",
        user="admin",
        password="CS4366Group",
        database="lecture-listener-database"
    )

    mycursor = mydb.cursor()
    sql = "DELETE FROM lecture WHERE lecture_id = %s"
    val = (lecture_id)
    mycursor.execute(sql, val)

    mydb.commit()