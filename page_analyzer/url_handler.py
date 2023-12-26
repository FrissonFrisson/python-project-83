import validators
from urllib.parse import urlparse


def validate_url(url):
    if not url:
        return {'status': False, 'msg': ('URL обязателен', 'danger')}
    elif not validators.url(url):
        return {'status': False, 'msg': ('Некорректный URL', 'danger')}
    return {'status': True, 'msg': ('Корректный URL', 'success')}


def normalize_urls(url):
    parsed_url = urlparse(url)
    normalize_url = f'{parsed_url.scheme}://{parsed_url.netloc}'
    return normalize_url
