import os

import mysql.connector
from dotenv import load_dotenv

# Connection settings come from environment variables or backend/.env (see .env.example).
load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))

DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
DB_PORT = int(os.getenv("DB_PORT", "3307"))  # start-mysql.sh runs MySQL on 3307
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD")
if DB_PASSWORD is None:
    raise RuntimeError("DB_PASSWORD is not set. Copy backend/.env.example to backend/.env and fill it in.")
DB_NAME = os.getenv("DB_NAME", "vaccine_management")


def get_connection():
    conn = mysql.connector.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
    )
    cursor = conn.cursor()
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
    cursor.execute(f"USE {DB_NAME}")
    cursor.close()
    conn.database = DB_NAME
    return conn


def init_tables():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS dose_details(
            did int,
            hid int,
            dose_name varchar(15),
            price int,
            dose_date date,
            slot1 int,
            slot2 int,
            slot3 int,
            slot4 int,
            slot1_used int default 0,
            slot2_used int default 0,
            slot3_used int default 0,
            slot4_used int default 0
        )
        """
    )
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS register_vaccine(
            regid int,
            adharno int,
            DOA1 date,
            DOA2 date default null,
            ndose int default 0,
            h_id1 int,
            amt1 int,
            h_id2 int,
            amt2 int default 0,
            marker1 varchar(2) default 'n',
            marker2 varchar(2) default 'n'
        )
        """
    )
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS user_register(
            adharno int,
            name varchar(25),
            age int,
            phone varchar(11)
        )
        """
    )
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS hospital(
            h_id int,
            hospital_name varchar(30),
            address varchar(50),
            pincode int,
            phone int,
            dr_name varchar(20)
        )
        """
    )
    conn.commit()
    cursor.close()
    conn.close()


def next_id(cursor, table, column):
    cursor.execute(f"SELECT MAX({column}) FROM {table}")
    result = cursor.fetchone()
    if result is None or result[0] is None:
        return 1
    return int(result[0]) + 1
