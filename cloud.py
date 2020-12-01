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

MyCursor = mydb.cursor(buffered=True)


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


def download_file(object_name, file_name):
    s3 = boto3.client('s3')
    s3.download_file('lecturelistener', object_name, file_name)


def add_user(username, email, password):
    sql = "SELECT * FROM user WHERE username = '" + username + "'"
    MyCursor.execute(sql)
    results = MyCursor.fetchone()

    if results:

        return 0

    else:

        sql = "INSERT INTO user (username,email,password,font_size,font_type,font_color,background_color) " \
              "VALUES (%s,%s,%s,%s,%s,%s,%s)"
        val = (username, email, password, "Medium", "Arial", "White", "Black")
        MyCursor.execute(sql, val)

        mydb.commit()

        return 1


def validate(username, password):
    sql = "SELECT * FROM user WHERE username = '" + username + "' AND password = '" + password + "'"
    MyCursor.execute(sql)
    results = MyCursor.fetchone()

    if results:

        return 1

    else:

        return 0


def add_lecture(username, lecture_id, date, length, course, audio, transcript):
    sql = "INSERT INTO lecture (username,lecture_id,date,length,course,audio,transcript) " \
          "VALUES (%s,%s,%s,%s,%s,%s,%s)"
    val = (username, lecture_id, date, length, course, audio, transcript)

    MyCursor.execute(sql, val)

    mydb.commit()


def delete_lecture(username, lecture_id):
    sql = "DELETE FROM lecture WHERE username = %s AND lecture_id = %s"
    val = (username, lecture_id)

    MyCursor.execute(sql, val)

    mydb.commit()


def add_timestamp(lecture_id, time):
    sql = "INSERT INTO users (lecture_id,time) VALUES (%s,%s)"
    val = (lecture_id, time)
    MyCursor.execute(sql, val)

    mydb.commit()


def delete_timestamp(lecture_id):
    sql = "DELETE FROM lecture WHERE lecture_id = %s"
    val = lecture_id
    MyCursor.execute(sql, val)

    mydb.commit()


def get_lecture_id(username):
    sql = "SELECT lecture_id FROM lecture WHERE username = '" + username + "'"
    MyCursor.execute(sql)
    results = MyCursor.fetchall()
    mydb.commit()

    if len(results) == 000000:
        result = "0"
    else:
        results.sort()
        result = results[-1][0]
        result = result[(len(username)):]
    result = str(int(result) + 1)
    print(len(result))
    while len(result) != 6:
        result = "0" + result
    lecture_id = username + result
    return lecture_id


def get_lectures(username):
    sql = "SELECT date,course,length,lecture_id FROM lecture WHERE username = '" + username + "'"
    MyCursor.execute(sql)
    results = MyCursor.fetchall()

    mydb.commit()
    return results


def update_settings(username, font_size, font_type, font_color, background_color):
    if font_size != "NULL":
        sql = "UPDATE customers SET font_size = %s WHERE username = %s"
        val = (font_size, username)
        MyCursor.execute(sql, val)
    if font_type != "NULL":
        sql = "UPDATE customers SET font_type = %s WHERE username = %s"
        val = (font_type, username)
        MyCursor.execute(sql, val)
    if font_color != "NULL":
        sql = "UPDATE customers SET font_color = %s WHERE username = %s"
        val = (font_color, username)
        MyCursor.execute(sql, val)
    if background_color != "NULL":
        sql = "UPDATE customers SET background_color = %s WHERE username = %s"
        val = (background_color, username)
        MyCursor.execute(sql, val)

    mydb.commit()


def update_course(username, lecture_id, course):
    sql = "UPDATE lectures SET course = %s WHERE username = %s AND lecture_id = %s"
    val = (course, username, lecture_id)

    MyCursor.execute(sql, val)

    mydb.commit()
