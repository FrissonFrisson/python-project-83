from flask import Flask, request, render_template
from flask import url_for, flash, abort, redirect
import os
import requests
from page_analyzer.utils import validate_url, normalize_url, parse_tags
from page_analyzer import db
from dotenv import load_dotenv


load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/urls', methods=['POST'])
def check_url():
    conn = db.connect(DATABASE_URL)
    raw_url = request.form['url']
    validate_error = validate_url(raw_url)
    if validate_error:
        flash(*validate_error)
        return render_template('index.html'), 422
    normalized_url = normalize_url(raw_url)
    url_info = db.get_url_by_name(conn, normalized_url)
    if url_info:
        db.close(conn)
        flash('Страница уже существует', 'info')
        return redirect(url_for('get_page_url', id=url_info.id))
    else:
        id = db.add_url(conn, normalized_url)
        db.close(conn)
        flash('Страница успешно добавлена', 'success')
        return redirect(url_for('get_page_url', id=id))


@app.route('/urls/<int:id>')
def get_page_url(id):
    conn = db.connect(DATABASE_URL)
    url = db.get_url_by_id(conn, id)
    url_checks = db.get_url_checks(conn, id)
    db.close(conn)
    if not url:
        return abort(404)
    return render_template(
        'page_url.html',
        url=url,
        url_checks=url_checks
    )


@app.get('/urls')
def get_page_urls():
    conn = db.connect(DATABASE_URL)
    urls = db.get_urls(conn)
    db.close(conn)
    return render_template('urls.html', urls=urls)


@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(error):
    return render_template('500.html'), 500


@app.route('/urls/<int:id>/checks', methods=['POST'])
def url_checks(id):
    conn = db.connect(DATABASE_URL)
    url = db.get_url_by_id(conn, id)
    try:
        response = requests.get(url.name)
        status_code = response.status_code
        response.raise_for_status()
        tags = parse_tags(response.content)
        db.add_url_check(conn, id, status_code, tags)
        flash('Страница успешно проверена', 'success')
    except requests.exceptions.RequestException:
        flash('Произошла ошибка при проверке', 'danger')
    db.close(conn)
    return redirect(url_for('get_page_url', id=id))
