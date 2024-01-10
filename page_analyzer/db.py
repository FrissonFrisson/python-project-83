import psycopg2
import psycopg2.extras
import os
from datetime import datetime
from dotenv import load_dotenv


load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')


def connect():
    conn = psycopg2.connect(DATABASE_URL)
    return conn


def close(conn):
    conn.close()


def get_url_by_name(conn, url):
    with conn.cursor() as cur:
        cur.execute('''SELECT 
                    id, name, created_at 
                    FROM urls 
                    WHERE name = %s''', (url,))
        result = cur.fetchone()
    if not result:
        return None
    id, name, date = result
    url_check = {'id': id, 'name': name, 'date': date}
    return url_check


def add_url(conn, url):
    with conn.cursor() as cur:
        cur.execute('''INSERT INTO urls (name, created_at)
                    VALUES (%s, %s) RETURNING id''', (url, datetime.now()))
        conn.commit()
        id = cur.fetchone()[0]
    return id


def get_url_by_id(conn, id):
    with conn.cursor(cursor_factory=psycopg2.extras.NamedTupleCursor) as cur:
        cur.execute('''SELECT id, name, created_at FROM urls
                    WHERE id = %s''', (id,))
        rows = cur.fetchone()
    return rows


def get_id_url(conn, url):
    with conn.cursor() as cur:
        cur.execute('SELECT id FROM urls WHERE name = %s', (url,))
        rows = cur.fetchone()
    return rows[0]


def get_urls(conn):
    with conn.cursor() as cur:
        cur.execute('''SELECT id, name FROM urls ORDER BY id DESC''')
        urls = cur.fetchall()
        cur.execute('''SELECT 
                    url_id, status_code, MAX(created_at) 
                    FROM url_checks 
                    GROUP BY url_id, status_code''')
        checks_urls = cur.fetchall()
        id_checks = {id: {'status': status, 'date': date} 
                     for id, status, date in checks_urls}
        result = []
        for id, name in urls:
            urls_dict = {
                'id': id,
                'name':name
            }
            if id in id_checks:
                urls_dict['status_code'] = id_checks.get(id).get('status')
                urls_dict['date'] = id_checks.get(id).get('date')  
            result.append(urls_dict)
    return result


def add_check_info(conn, url_id, status_code, h1, title, description):
    with conn.cursor() as cur:
        cur.execute('''INSERT INTO url_checks
                    (url_id, status_code, h1, title, description, created_at)
                    VALUES (%s, %s, %s, %s, %s, %s)''',
                    (url_id, status_code, h1, 
                     title, description, datetime.now()))
        conn.commit()

def get_url_checks(conn, id):
    with conn.cursor() as cur:
        cur.execute('''SELECT 
                    id, status_code, h1, title, description, created_at
                    FROM url_checks
                    WHERE url_id = %s
                    ORDER BY id DESC''',
                    (id,)
                    )
        rows = cur.fetchall()
    return rows
