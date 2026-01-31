from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from conftest import EXPECTED_URL


class LoginPage: # Класс для работы со страницей входа
    
    def __init__(self, driver):
        self.driver = driver
        self.driver.set_page_load_timeout(30) # Ожидание загрузки страницы
    
    def open(self): # Открытие страницы входа
        self.driver.get(EXPECTED_URL)
        try:
            WebDriverWait(self.driver, 10).until(
                EC.url_to_be(EXPECTED_URL)
            )
        except TimeoutException:
            CURRENT_URL = self.driver.current_url
            raise AssertionError(
                f"Ошибка открытия страницы!\n"
                f"Ожидалось: {EXPECTED_URL}\n"
                f"Фактически: {CURRENT_URL}\n"
                f"Страница не загрузилась или произошёл редирект на другую страницу."
            )
        return self

    
    def enter_username(self, username): # Ввод логина
        user_name = self.driver.find_element(By.ID, "user-name")
        user_name.clear()
        user_name.send_keys(username)
        return self
    
    def enter_password(self, password): # Ввод пароля
        password_field = self.driver.find_element(By.ID, "password")
        password_field.clear()
        password_field.send_keys(password)
        return self
    
    def click_login(self): # Нажатие на кнопку "Login"
        self.driver.find_element(By.ID, "login-button").click()
        return self
    
    def login(self, username, password): # Полный процесс входа
        self.enter_username(username)
        self.enter_password(password)
        self.click_login()
        return self
    
    
    def get_current_url(self): # Получение текущего URL
        return self.driver.current_url
    
            
    def get_error_message(self, timeout=2): # Получения текста ошибки
        try:
            error_element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "[data-test='error']"))
            )
            return error_element.text.strip()
        except TimeoutException:
            return ""