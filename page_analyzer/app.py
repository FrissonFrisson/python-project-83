from page_analyzer import app


@app.route('/')
def hello_world():
    return 'Welcome to  Flask!'
