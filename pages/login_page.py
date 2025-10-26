from selenium.webdriver.common.by import By
from base.base_page import BasePage

class LoginPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.username_field = (By.XPATH, "//input[@name='username']")
        self.password_field = (By.XPATH, "//input[@name='password']")
        self.login_btn = (By.XPATH, "//button[@type='submit']")
        self.require_username = (By.XPATH, "//input[@name='username']/following::span[text()='Required'][1]")
        self.require_password = (By.XPATH, "//input[@name='password']/following::span[text()='Required'][1]")
        self.invalid_credentials = (By.XPATH, "//p[text()='Invalid credentials']")
    
    def verify_username_field_is_displayed(self):
        return self.is_displayed(self.username_field)

    def verify_password_field_is_displayed(self):
        return self.is_displayed(self.password_field)

    def login(self, username, password):
        self.type(self.username_field, username)
        self.type(self.password_field, password)
        self.get_element(self.login_btn).click()

    def click_login_btn(self):
        self.get_element(self.login_btn).click()
    
    def verify_require_username_displayed(self):
        return self.is_displayed(self.require_username)
    
    def verify_require_password_displayed(self):
        return self.is_displayed(self.require_password)
    
    def vefiry_invalid_credentials_displayed(self):
        return self.is_displayed(self.invalid_credentials)
    



