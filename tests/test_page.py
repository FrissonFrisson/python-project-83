import pytest
from page_analyzer import app as my_app

@pytest.fixture()
def app():
    app = my_app
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///test_db.sqlite"
    }
    )


    # other setup can go here

    yield app

    # clean up / reset resources here


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()


def test_index_page(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b' <input type="text" name="url" placeholder="https://www.example.com"' in response.data


def test_analyze_url(client):
    response = client.post('/urls', data={'url': 'https://www.example.com'})
    assert response.status_code == 200
    assert b'https://www.example.com' in response.data
    response = client.post('/urls', data={'url': 'https://www.example.com'})
    assert response.status_code == 302
    assert b'https://www.example.com' in response.data


