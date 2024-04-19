import os

import requests
from dotenv import load_dotenv
from flask import Flask, render_template, request, flash, url_for, redirect

from page_analyzer.parser import parse_page
from .db import (add_url, get_url_by_id, get_all_urls, get_url_by_name,
                 add_url_check, get_checks_by_url_id)
from .validators import validate, normalize

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['DATABASE_URL'] = os.getenv('DATABASE_URL')
app.config['DEBUG'] = os.getenv('DEBUG')


@app.get('/')
def get_index():
    return render_template('index.html')


@app.post('/urls')
def create_url():
    url = request.form.get('url')
    error = validate(url)
    if error:
        flash(error, 'alert-danger')
        return render_template('index.html'), 422

    url = normalize(url)
    url_in_db = get_url_by_name(url)
    if url_in_db:
        url_id = url_in_db.id
        flash('Страница уже существует', 'alert-info')
    else:
        url_id = add_url(url)
        flash('Страница успешно добавлена', 'alert-success')
    return redirect(url_for('get_url', url_id=url_id))


@app.get('/urls')
def get_urls():
    urls = get_all_urls()
    return render_template('url_list.html', items=urls)


@app.get('/urls/<int:url_id>')
def get_url(url_id):
    url = get_url_by_id(url_id)
    if url is None:
        return render_template('404.html'), 404
    checks = get_checks_by_url_id(url_id)
    return render_template('url_detail.html', url=url, checks=checks)


@app.post('/urls/<int:url_id>/checks')
def url_checks(url_id):
    url = get_url_by_id(url_id)
    try:
        response = requests.get(url.name)
        response.raise_for_status()
    except requests.exceptions.RequestException:
        flash('Ошибка при проверке', 'alert-danger')
        return redirect(url_for('get_url', url_id=url_id))

    check_data = parse_page(response.text)
    check_data['url_id'] = url_id
    check_data['status_code'] = response.status_code

    add_url_check(check_data)
    flash('Страница успешно проверена', 'alert-success')
    return redirect(url_for('get_url', url_id=url_id))


if __name__ == '__main__':
    app.run()
