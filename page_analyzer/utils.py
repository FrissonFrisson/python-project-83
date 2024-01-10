import validators
from urllib.parse import urlparse
from bs4 import BeautifulSoup


def validate_url(url):
    if not url:
        return 'URL обязателен', 'danger'
    elif not validators.url(url):
        return 'Некорректный URL', 'danger'


def normalize_url(url):
    parsed_url = urlparse(url)
    normalize_url = f'{parsed_url.scheme}://{parsed_url.netloc}'
    return normalize_url


def parse_tags(content):
    soup = BeautifulSoup(content, "html.parser")
    title = soup.find("title").get_text() if soup.find("title") else ''
    header = soup.find("h1").get_text() if soup.find("h1") else ''
    description = soup.find("meta", attrs={"name": "description"})
    description = description['content'] if description else ''
    return header, title, description
