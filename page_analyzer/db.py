import os
from datetime import datetime

from dotenv import load_dotenv
from psycopg2 import connect
from psycopg2.extras import NamedTupleCursor

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')


class DatabaseConnection:
    def __enter__(self):
        self.connection = connect(DATABASE_URL)
        self.cursor = self.connection.cursor(cursor_factory=NamedTupleCursor)
        return self.cursor

    def __exit__(self, exc_type, exc_value, traceback):
        self.cursor.close()
        self.connection.commit()
        self.connection.close()


def add_url(url):
    with DatabaseConnection() as cursor:
        query = ('INSERT INTO urls (name, created_at) VALUES (%s, %s) '
                 'RETURNING id')
        values = (url, datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        cursor.execute(query, values)
        return cursor.fetchone().id


def get_url_by_name(url):
    with DatabaseConnection() as cursor:
        query = 'SELECT * FROM urls WHERE name = (%s)'
        cursor.execute(query, (url,))
        data = cursor.fetchone()
        return data


def get_url_by_id(url_id):
    with DatabaseConnection() as cursor:
        query = 'SELECT * FROM urls WHERE id = (%s)'
        cursor.execute(query, (url_id,))
        data = cursor.fetchone()
        return data


def get_all_urls():
    with DatabaseConnection() as cursor:
        query = ('SELECT urls.id AS id, urls.name AS name, '
                 'urls.created_at AS last_check, '
                 'status_code '
                 'FROM urls '
                 'LEFT JOIN url_checks '
                 'ON urls.id = url_checks.url_id '
                 'AND url_checks.id = ('
                 'SELECT max(id) FROM '
                 'url_checks WHERE urls.id = url_checks.url_id) '
                 'ORDER BY urls.id DESC;')
        cursor.execute(query)
        urls = cursor.fetchall()
        return urls


def add_url_check(check_data):
    with DatabaseConnection() as cursor:
        query = ('INSERT INTO url_checks '
                 '(url_id, status_code, h1, title, description, created_at) '
                 'VALUES (%s, %s, %s, %s, %s, %s)')
        values = (check_data.get('url_id'), check_data.get('status_code'),
                  check_data.get('h1', ''), check_data.get('title', ''),
                  check_data.get('description', ''),
                  datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        cursor.execute(query, values)


def get_checks_by_url_id(url_id):
    with DatabaseConnection() as cursor:
        query = 'SELECT * FROM url_checks WHERE url_id=(%s) ORDER BY id DESC'
        cursor.execute(query, (url_id,))
        checks = cursor.fetchall()
        return checks
