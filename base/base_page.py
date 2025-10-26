from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class BasePage:
    def __init__(self, driver):
        self.driver = driver

    def get_element(self, locator):
        element = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(locator))
        return element
    
    def get_elements(self, locator):
        elements = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(locator))
        return elements
    
    def type(self, locator, text):
        element = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(locator))
        element.clear()
        element.send_keys(text)

    def is_displayed(self, locator):
        element = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(locator))
        return element.is_displayed()

    def click_by_js(self, locator):
        element = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(locator))
        self.driver.execute_script("arguments[0].click();", element)