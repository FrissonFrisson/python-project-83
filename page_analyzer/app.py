from flask import Flask, request, render_template
from flask import url_for, flash, abort, redirect
import os
from bs4 import BeautifulSoup
import requests
from page_analyzer.url_handler import validate_url, normalize_urls
from page_analyzer import db

SECRET_KEY = os.getenv('SECRET_KEY')
app = Flask(__name__)
app.secret_key = SECRET_KEY


@app.route('/')
def index_page():
    return render_template('index.html')


@app.route('/urls', methods=['POST'])
def analyze_url():
    url = request.form['url']
    validate = validate_url(url)
    if validate['status'] is False:
        flash(*validate['msg'])
        return render_template('index.html'), 422
    url = normalize_urls(url)

    if db.check_in_urls(url):
        id = db.get_id_url(url)
        flash('Страница уже существует', 'info')
        return redirect(url_for('get_page_url', id=id))
    else:
        db.add_url(url)
        id = db.get_id_url(url)
        flash('Страница успешно добавлена', 'success')
        return redirect(url_for('get_page_url', id=id))


@app.route('/urls/<int:id>')
def get_page_url(id):
    url_info = db.get_url_info(id)
    checks_info = db.get_checks_list(id)
    if not url_info:
        return abort(404)
    return render_template(
        'page_url.html',
        url_info=url_info,
        checks_info=checks_info
        )


@app.get('/urls')
def get_page_urls():
    list_urls = db.get_list_urls()
    return render_template('urls.html', urls=list_urls)


@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404


@app.route('/urls/<int:id>/checks', methods=['POST'])
def url_checks(id):
    url_info = db.get_url_info(id)
    try:
        r = requests.get(url_info['name'])
        flash('Страница успешно проверена', 'success')
        html = r.content
        soup = BeautifulSoup(html, "html.parser")
        title = soup.find("title")
        header = soup.find("h1")
        description = soup.find("meta", attrs={"name": "description"})
        status_code = r.status_code
        h1 = header.get_text() if header else ''
        title = title.get_text() if title else ''
        description = description['content'] if description else ''
        db.add_check_info(id, status_code, h1, title, description)
    except requests.exceptions.RequestException:
        flash('Произошла ошибка при проверке', 'danger')
    return redirect(url_for('get_page_url', id=id))
