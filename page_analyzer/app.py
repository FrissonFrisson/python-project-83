from flask import Flask, request, render_template, url_for, flash, abort, redirect
import os
from page_analyzer.url_handler import validate_url, normalize_urls
from page_analyzer import db
from dotenv import load_dotenv

SECRET_KEY = os.getenv('SECRET_KEY')
app = Flask(__name__)
app.secret_key = SECRET_KEY


@app.route('/')
def index_page():
    return render_template('index.html')


@app.route('/urls', methods=['POST'])
def analyze_url():
    conn = db.connect()
    url = request.form['url']
    validate = validate_url(url)
    if validate['status'] is False:
        flash(*validate['msg'])
        return render_template('index.html')
    url = normalize_urls(url)

    if db.check_in_urls(url):
        id = db.get_id_url(url)
        flash('Страница уже существует','info')
        return redirect(url_for('get_page_url', id = id))
    else:
        db.add_url(url)
        id = db.get_id_url(url)
        flash('Страница успешно добавлена','success')
        return redirect(url_for('get_page_url', id = id))


@app.route('/urls/<int:id>')
def get_page_url(id):
    url_info = db.get_url_info(id)
    if not url_info:
        return abort(404)
    id, name, date = url_info
    return render_template('page_url.html', id=id, name=name, date=date)


@app.get('/urls')
def get_page_urls():
    list_urls = db.get_list_urls()
    return render_template('urls.html', urls = list_urls)


@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404
