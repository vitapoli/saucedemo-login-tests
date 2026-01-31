import pytest
import allure
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.login_page import LoginPage
from conftest import PASSWORD, VALID_USERS, LOCKED_USER, ERROR_INVALID_PASSWORD, ERROR_LOCKED_USER, ERROR_EMPTY_FIELDS, INVENTORY_URL

class TestLogin:
    
    @allure.title("ТЕСТ_1 Успешный логин и пароль")
    def test_successful_login(self, driver):
        login_page = LoginPage(driver)
        
        with allure.step("Открыть страницу"):
            login_page.open()
            
        with allure.step("Войти с успешными данными"):    
            login_page.login("standard_user", PASSWORD) 
            
        with allure.step("Проверить переход"):
            assert login_page.get_current_url() == INVENTORY_URL, \
                f"Переход не произошел. Текущий URL: {login_page.get_current_url()}"
        
        
    @pytest.mark.parametrize("username", VALID_USERS)
    @allure.title("ТЕСТ_2 Логин с неверным паролем")
    def test_invalid_password(self, driver, username): 
        login_page = LoginPage(driver)
        
        with allure.step("Открыть страницу"):
            login_page.open()
            
        with allure.step("Войти с неверным паролем"): 
            login_page.login(username, "wrong_password")
        
        with allure.step("Проверить ошибку неверного пароля"):
            error_text = login_page.get_error_message(timeout=5)
            assert error_text == ERROR_INVALID_PASSWORD, \
                f"Неверное сообщение об ошибке. Ожидалось: '{ERROR_INVALID_PASSWORD}', получено: '{error_text}'"
    
    @allure.title("ТЕСТ_3 Логин заблокированного пользователя")
    def test_login_locked_user(self, driver): 
        login_page = LoginPage(driver)
        
        with allure.step("Открыть страницу"):
            login_page.open()
            
        with allure.step("Войти с заблокированным логином"): 
            login_page.login(LOCKED_USER, PASSWORD)
        
        with allure.step("Проверить ошибку заблокированного пользователя"):
            error_text = login_page.get_error_message(timeout=5)
            assert error_text == ERROR_LOCKED_USER, \
            f"Неверное сообщение об ошибке. Ожидалось: '{ERROR_LOCKED_USER}', получено: '{error_text}'"
    
    @allure.title("ТЕСТ_4 Логин с пустыми полями")
    def test_login_with_empty_fields(self, driver): 
        login_page = LoginPage(driver)
    
        with allure.step("Открыть страницу"):
            login_page.open()
            
        with allure.step("Войти с пустыми полями"): 
            login_page.login("", "")
        
        with allure.step("Проверить ошибку пустых полей"):
            error_text = login_page.get_error_message(timeout=5)
            assert error_text == ERROR_EMPTY_FIELDS, \
            f"Неверное сообщение об ошибке. Ожидалось: '{ERROR_EMPTY_FIELDS}', получено: '{error_text}'"
        
    @allure.title("ТЕСТ_5 Логин пользователя performance_glitch_user")
    def test_login_performance_glitch_user(self, driver): 
        login_page = LoginPage(driver)
        
        with allure.step("Открыть страницу"):
            login_page.open()
            
        with allure.step("Войти в систему"):     
            login_page.login("performance_glitch_user", PASSWORD)
        
            WebDriverWait(driver, 20).until(
                EC.url_contains("inventory.html")
            )
        
        with allure.step("Проверить переход"):
            assert login_page.get_current_url() == INVENTORY_URL, \
                f"Переход не произошел. Текущий URL: {login_page.get_current_url()}"
        
        