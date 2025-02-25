import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app  # Импортируем Flask-приложение


def test_index():
    tester = app.test_client()  # Создаем тест-клиент
    response = tester.get('/')  # Делаем GET-запрос на главную страницу

    assert b"Levchenko Alexey Viktorovich" in response.data  # Проверяем наличие имени в ответе
    assert b"Group: DOS24-onl" in response.data  # Проверяем наличие группы
    assert b"Topic: webserver" in response.data  # Проверяем наличие темы
    assert b"IP Address:" in response.data  # Проверяем, что IP-адрес отображается


def test_images_exist():
    tester = app.test_client()
    response = tester.get('/')

    assert b"<img src=\"" in response.data  # Проверяем, что на странице есть изображения


def test_page_title():
    tester = app.test_client()
    response = tester.get('/')

    assert b"<title>Information</title>" in response.data  # Проверяем, что заголовок страницы корректный


test_index()
test_images_exist()
test_page_title()
