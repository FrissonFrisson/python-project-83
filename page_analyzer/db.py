import psycopg2
import os
import datetime
from dotenv import load_dotenv

DATENOW = datetime.datetime.now().date()
load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')


def connect():
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    return conn, cur


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
    cur.execute('''INSERT INTO urls (name, created_at)
                VALUES (%s, %s)''', (url, datetime.datetime.now()))
    conn.commit()
    conn.close()


def get_url_info(id):
    conn, cur = connect()
    cur.execute('''SELECT id, name, created_at FROM urls
                WHERE id = %s''', (id,))
    rows = cur.fetchone()
    conn.close()
    if rows:
        id, name, date = rows
        url_dict = {'id': id, 'name': name, 'date': date}
        return url_dict
    return {}


def get_id_url(url):
    conn, cur = connect()
    cur.execute('SELECT id FROM urls WHERE name = %s', (url,))
    rows = cur.fetchone()
    conn.close()
    return rows[0]


def get_list_urls():
    conn, cur = connect()
    cur.execute('''SELECT urls.id, urls.name, MAX(url_checks.created_at) AS created_at, url_checks.status_code
FROM urls
LEFT JOIN url_checks ON urls.id = url_checks.url_id
GROUP BY urls.id, urls.name, url_checks.status_code
ORDER BY urls.id DESC;''')
    rows = cur.fetchall()
    conn.close()
    return rows


def add_check_info(url_id, status_code, h1, title, description):
    conn, cur = connect()
    cur.execute('''INSERT INTO url_checks (url_id, status_code, h1, title, description, created_at)
                VALUES (%s, %s, %s, %s, %s, %s)''', (url_id, status_code, h1, title, description, datetime.datetime.now()))
    conn.commit()
    conn.close()


def get_checks_list(id):
    conn, cur = connect()
    cur.execute('SELECT id, status_code, h1, title, description, created_at FROM url_checks WHERE url_id = %s ORDER BY created_at DESC', (id,))
    rows = cur.fetchall()
    conn.close()
    return rows