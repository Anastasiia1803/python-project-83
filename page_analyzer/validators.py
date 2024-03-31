from urllib.parse import urlparse
import validators


MAX_URL_LENGTH = 255


def validator(url):
    if not url:
        return 'Поле URL обязательно к заполнению'
    elif len(url) > MAX_URL_LENGTH:
        return f'URL превышает {MAX_URL_LENGTH} символов'
    elif not validators.url(url):
        return 'Некорректный URL'


def normalizer(url):
    data = urlparse(url)
    return data.scheme + '://' + data.netloc
