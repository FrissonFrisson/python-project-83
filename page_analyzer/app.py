from flask import Flask, request, render_template

app = Flask(__name__)


@app.route('/')
def index_page():
    return render_template(
        'index.html'
    )


@app.route('/urls', methods=['POST'])
def analyze_url():
    url = request.form['url']
    # здесь можно добавить логику для анализа URL
    return render_template('urls.html', url=url)
