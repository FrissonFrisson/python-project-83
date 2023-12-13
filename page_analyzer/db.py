import psycopg2
import os
import datetime
from dotenv import load_dotenv


load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')


def connect():
    try:
        # пытаемся подключиться к базе данных
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        return conn, cur
    except:
        # в случае сбоя подключения будет выведено сообщение  в STDOUT
        print('Can`t establish connection to database')


def check_in_urls(url):
    conn, cur = connect()
    cur.execute('SELECT urls FROM urls WHERE name = %s', (url,))
    rows = cur.fetchall()
    conn.close()
    if rows:
        return True
    else:
        return False
    

def add_url(url):
    conn, cur = connect()
    cur.execute('INSERT INTO urls (name, created_at) VALUES (%s, %s)', (url,datetime.datetime.now()))
    conn.commit()
    conn.close()


def get_url_info(id):
    conn, cur = connect()
    cur.execute('SELECT id, name, created_at FROM urls WHERE id = %s', (id,))
    rows = cur.fetchone()
    conn.close()
    return rows


def get_id_url(url):
    conn, cur = connect()
    cur.execute('SELECT id FROM urls WHERE name = %s', (url,))
    rows = cur.fetchone()
    conn.close()
    return rows[0]


def get_list_urls():
    conn, cur = connect()
    cur.execute('SELECT id, name, created_at FROM urls')
    rows = cur.fetchall()
    conn.close()
    return rows