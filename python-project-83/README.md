# Page Analyzer
***

__Page Analyzer__ - анализирует указанные страницы на SEO-пригодность.

![Hexlet Badge](https://img.shields.io/badge/Hexlet-116EF5?logo=hexlet&logoColor=fff&style=for-the-badge)
[![Actions Status](https://github.com/Anastasiia1803/python-project-83/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/Anastasiia1803/python-project-83/actions)
[![Actions Status](https://github.com/Anastasiia1803/python-project-83/actions/workflows/linter.yml/badge.svg)](https://github.com/Anastasiia1803/python-project-83/actions)

## Установка

1. Склонируйте репозиторий с проектом на ваше локальное устройство:
```
git clone git@github.com:Anastasiia1803/python-project-83.git
```
2. Перейдите в директорию проекта:
```
cd python-project-83
```
3. Установите необходимые зависимости с помощью Poetry:
```
make install
```
4. Создайте файл .env, который будет содержать ваши конфиденциальные настройки:

```
cp .env.example .env
```

Откройте файл .env и замените значение ключей SECRET_KEY и DATABASE_URL.

5. Затем запустите команды из database.sql в SQL-консоли вашей базы данных, чтобы создать необходимые таблицы.

***

## Использование
1. Для запуска сервера Flask с помощью Gunicorn выполните команду:

```
make start
```
По умолчанию сервер будет доступен по адресу http://0.0.0.0:8000.

2. Также можно запустить сервер локально в режиме разработки с активным отладчиком:

```
make dev
```
Сервер для разработки будет доступен по адресу http://127.0.0.1:5000.

Чтобы добавить новый сайт, введите его адрес в форму на главной странице. Введенный адрес будет проверен и добавлен в базу данных.

После добавления сайта можно начать его проверку. На странице каждого конкретного сайта появится кнопка, и нажав на нее, вы создадите запись в таблице проверки.

Все добавленные URL можно увидеть на странице /urls.

***
## Способы использования
Проект можно использовать локально и онлайн (например с помощью стороннего сервиса [render.com](https://dashboard.render.com/)).

***
## Демонстрация работы программы:
Демонстрационные проект доступен по  [ссылке](https://python-project-83-qe7c.onrender.com/).
***