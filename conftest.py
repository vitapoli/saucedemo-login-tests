"""import sys
import os

# Добавляем корень проекта в sys.path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))"""


import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

# ==================== КОНСТАНТЫ ДАННЫХ ====================

# Валидный пароль
PASSWORD = "secret_sauce"

# Список валидных пользователей
VALID_USERS = [
    "standard_user",
    "problem_user",
    "performance_glitch_user",
    "error_user",
    "visual_user"
]

# Заблокированный пользователь
LOCKED_USER = "locked_out_user"

# Сообщения об ошибках
ERROR_INVALID_PASSWORD = "Epic sadface: Username and password do not match any user in this service"
ERROR_LOCKED_USER = "Epic sadface: Sorry, this user has been locked out."
ERROR_EMPTY_FIELDS = "Epic sadface: Username is required"

# URL приложения
EXPECTED_URL = "https://www.saucedemo.com/"
INVENTORY_URL = "https://www.saucedemo.com/inventory.html"


# ==================== ФИКСТУРЫ ====================

@pytest.fixture(scope="function")
def driver():
    """
    Фикстура для инициализации WebDriver Chrome в headless режиме.
    Автоматически закрывает браузер после завершения теста.
    """
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")               # Современный headless режим - "без браузера"
    chrome_options.add_argument("--no-sandbox")                 # Запускаем Chrome без "песочницы"
    chrome_options.add_argument("--disable-dev-shm-usage")      # Отключаем использование разделяемой памяти
    chrome_options.add_argument("--disable-gpu")                # Отключаем использование GPU
    
    # Дополнительные опции для стабильности в Docker
    chrome_options.add_argument("--disable-setuid-sandbox")
    chrome_options.add_argument("--remote-debugging-port=9222")
    
    
    driver = webdriver.Chrome(options=chrome_options)
    driver.set_page_load_timeout(15)
    
    # Передаём объект DRIVER в тестовую функцию
    yield driver
    
    # Закрываем браузер после выполнения теста
    driver.quit()