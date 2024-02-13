import psycopg2
import psycopg2.extras
from datetime import datetime


def connect(databseurl):
    conn = psycopg2.connect(databseurl)
    return conn


def close(conn):
    conn.close()


def get_url_by_name(conn, url):
    with conn.cursor(cursor_factory=psycopg2.extras.NamedTupleCursor) as cur:
        cur.execute('''SELECT
                    id, name, created_at
                    FROM urls
                    WHERE name = %s''', (url,))
        url_info = cur.fetchone()
    return url_info


def get_url_by_id(conn, id):
    with conn.cursor(cursor_factory=psycopg2.extras.NamedTupleCursor) as cur:
        cur.execute('''SELECT
                    id, name, created_at
                    FROM urls
                    WHERE id = %s''', (id,))
        url_info = cur.fetchone()
    return url_info


def add_url(conn, url):
    with conn.cursor() as cur:
        cur.execute('''INSERT INTO urls (name, created_at)
                    VALUES (%s, %s) RETURNING id''', (url, datetime.now()))
        conn.commit()
        id = cur.fetchone()[0]
    return id


def get_urls(conn):
    with conn.cursor(cursor_factory=psycopg2.extras.NamedTupleCursor) as cur:
        cur.execute('''SELECT id, name FROM urls ORDER BY id DESC''')
        urls = cur.fetchall()
        cur.execute('''SELECT
                    url_id, status_code, MAX(created_at) as date
                    FROM url_checks
                    GROUP BY url_id, status_code''')
        checks_urls = cur.fetchall()
        id_checks = {url_check.url_id:
                     {'status': url_check.status_code,
                      'date': url_check.date
                      }
                     for url_check in checks_urls
                     }
        result = []
        for url_info in urls:
            urls = {
                'id': url_info.id,
                'name': url_info.name
            }
            if url_info.id in id_checks:
                urls['status_code'] = id_checks.get(url_info.id).get('status')
                urls['date'] = id_checks.get(url_info.id).get('date')
            result.append(urls)
    return result


def add_url_check(conn, url_id, status_code, tags):
    with conn.cursor() as cur:
        cur.execute('''INSERT INTO url_checks
                    (url_id, status_code, h1, title, description, created_at)
                    VALUES (%s, %s, %s, %s, %s, %s)''',
                    (url_id,
                     status_code,
                     tags.get('h1', ''),
                     tags.get('title', ''),
                     tags.get('description', ''),
                     datetime.now())
                    )
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
