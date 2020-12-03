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


def upload_file(file_name, object_name):
    # Upload the file
    s3_client = boto3.client('s3')
    try:
        s3_client.upload_file(file_name, 'lecturelistener', object_name)
        return 1
    except ClientError as e:
        logging.error(e)
        return 0


def download_file(object_name, file_name):
    s3 = boto3.client('s3')
    s3.download_file('lecturelistener', object_name, file_name)


def check_storage(object_name):
    s3 = boto3.client('s3')
    try:
        s3.head_object(Bucket='lecturelistener', Key=object_name)
        return 1
    except ClientError:
        return 0


def delete_file(object_name):
    s3 = boto3.client('s3')
    s3.delete_object(Bucket='lecturelistener', Key=object_name)


def add_user(username, email, password):
    sql = "SELECT * FROM user WHERE username = '" + username + "'"
    mycursor.execute(sql)
    results = mycursor.fetchone()
    if results:
        return 0
    else:
        sql = "INSERT INTO user (username,email,password,font_size,font_type,font_color,background_color) " \
              "VALUES (%s,%s,%s,%s,%s,%s,%s)"
        val = (username, email, password, "Medium", "Arial", "White", "Black")
        mycursor.execute(sql, val)
        mydb.commit()
        return 1


def validate(username, password):
    sql = "SELECT * FROM user WHERE username = '" + username + "' AND password = '" + password + "'"
    mycursor.execute(sql)
    results = mycursor.fetchone()
    if results:
        return 1
    else:
        return 0


def add_lecture(username, lecture_id, date, length, course):
    sql = "INSERT INTO lecture (username,lecture_id,date,length,course) VALUES (%s,%s,%s,%s,%s)"
    val = (username, lecture_id, date, length, course)
    mycursor.execute(sql, val)
    mydb.commit()
    return val[1]


def delete_lecture(lecture_id):
    sql = "DELETE FROM lecture WHERE lecture_id = '" + lecture_id + "'"
    mycursor.execute(sql)
    mydb.commit()


def get_lecture_id(username):
    sql = "SELECT lecture_id FROM lecture WHERE username = '" + username + "'"
    mycursor.execute(sql)
    results = mycursor.fetchall()
    mydb.commit()
    if len(results) == 0:
        return username + '000000'
    results.sort()
    result = results[-1][0]
    result = result[(len(username)):]
    result = str(int(result) + 1)
    while len(result) != 6:
        result = "0" + result
    return username + result


def get_lectures(username):
    sql = "SELECT date,course,length,lecture_id,audio,transcript FROM lecture WHERE username = '" \
          + username + "'"
    mycursor.execute(sql)
    results = mycursor.fetchall()
    mydb.commit()
    return results


def update_settings(username, font_size, font_type, font_color, background_color):
    if font_size != "NULL":
        sql = "UPDATE customers SET font_size = %s WHERE username = %s"
        val = (font_size, username)
        mycursor.execute(sql, val)
    if font_type != "NULL":
        sql = "UPDATE customers SET font_type = %s WHERE username = %s"
        val = (font_type, username)
        mycursor.execute(sql, val)
    if font_color != "NULL":
        sql = "UPDATE customers SET font_color = %s WHERE username = %s"
        val = (font_color, username)
        mycursor.execute(sql, val)
    if background_color != "NULL":
        sql = "UPDATE customers SET background_color = %s WHERE username = %s"
        val = (background_color, username)
        mycursor.execute(sql, val)
    mydb.commit()


def update_course(lecture_id, course):
    sql = "UPDATE lectures SET course = %s WHERE lecture_id = %s"
    val = (course, lecture_id)
    mycursor.execute(sql, val)
    mydb.commit()
