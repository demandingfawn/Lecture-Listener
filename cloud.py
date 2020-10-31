import mysql.connector
import logging
import boto3
from botocore.exceptions import ClientError

mydb = mysql.connector.connect(
    host="lecture-listener-database.ced4pprbqpl5.us-east-2.rds.amazonaws.com",
    user="admin",
    password="CS4366Group",
    database='Lecture_Listener'
)

mycursor = mydb.cursor(buffered=True)

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


def add_user(username,email,password):

    sql = "SELECT * FROM user WHERE username = '%s'"
    val = username
    rows=mycursor.execute(sql,val)
    #results = mycursor.fetchone()
    print("result=",rows,"username=",val)

    if rows is not None:

        return 0

    else:
        sql = "INSERT INTO user (username,email,password,font_size,font_type,font_color,background_color) VALUES (%s,%s,%s,%s,%s,%s,%s)"
        val = (username, email, password, "12", "Calabri", "White", "Black")
        mycursor.execute(sql, val)

        mydb.commit()

        return 1


def add_lecture(username,lecture_id,date,length,course,audio,transcript):

    sql = "INSERT INTO users (user_id,lecture_id,date,length,course,audio,transcript) VALUES (%s,%s,%s,%s,%s,%s,%s)"
    val = (username,lecture_id,date,length,course,audio,transcript)
    mycursor.execute(sql, val)

    mydb.commit()


def add_timestamp(lecture_id,time):

    sql = "INSERT INTO users (lecture_id,time) VALUES (%s,%s)"
    val = (lecture_id,time)
    mycursor.execute(sql, val)

    mydb.commit()


def update_settings(username, font_size, font_type, font_color, background_color):

    if (font_size != "NULL"):
        sql = "UPDATE customers SET font_size = %s WHERE user_id = %s"
        val = (font_size, username)
        mycursor.execute(sql, val)
    if (font_type != "NULL"):
        sql = "UPDATE customers SET font_type = %s WHERE user_id = %s"
        val = (font_type, username)
        mycursor.execute(sql, val)
    if (font_color != "NULL"):
        sql = "UPDATE customers SET font_color = %s WHERE user_id = %s"
        val = (font_color, username)
        mycursor.execute(sql, val)
    if (background_color != "NULL"):
        sql = "UPDATE customers SET background_color = %s WHERE user_id = %s"
        val = (background_color, username)
        mycursor.execute(sql, val)

    mydb.commit()


def update_settings(username,lecture_id,course):

    sql = "UPDATE customers SET course = %s WHERE user_id = %s AND lecture_id = %s"
    val = (course,username,lecture_id)
    mycursor.execute(sql, val)

    mydb.commit()


def delete_lecture(username,lecture_id):

    sql = "DELETE FROM lecture WHERE user_id = %s AND lecture_id = %s"
    val = (username,lecture_id)
    mycursor.execute(sql, val)

    mydb.commit()


def delete_timestamp(lecture_id):

    sql = "DELETE FROM lecture WHERE lecture_id = %s"
    val = (lecture_id)
    mycursor.execute(sql, val)

    mydb.commit()