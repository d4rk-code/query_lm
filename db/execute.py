import os
import mysql.connector as ms
from dotenv import load_dotenv

load_dotenv()

def execute(query):

    mydb = ms.connect(
        host="localhost",
        user=os.getenv("user"),
        password=os.getenv("password"),
        database=os.getenv("database")
    )

    cursor = mydb.cursor()

    try:

        cursor.execute(query)
        data = cursor.fetchall()

        return data

    except Exception as e:
        return f"error occured: {e}"

    finally:
        cursor.close()
        mydb.close()
