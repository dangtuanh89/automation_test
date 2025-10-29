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
        elements = WebDriverWait(self.driver, 10).until(EC.presence_of_all_elements_located(locator))
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

    def wait_and_click(self, locator, use_js_fallback: bool = True, timeout: int = 10):
        """
        Wait until the element is clickable and click it. If the element is not interactable
        (common in headless CI environments or when element is off-screen/overlapped),
        optionally fallback to a JS click.

        Args:
            locator: tuple locator (By, value)
            use_js_fallback: when True, if element_to_be_clickable fails or click raises
                             ElementNotInteractableException, a JS click will be performed.
            timeout: seconds to wait for clickable condition.
        """
        try:
            element = WebDriverWait(self.driver, timeout).until(EC.element_to_be_clickable(locator))
            element.click()
        except Exception:
            if use_js_fallback:
                # Ensure element is present then click via JS (scroll into view first)
                element = WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located(locator))
                try:
                    self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
                except Exception:
                    pass
                self.driver.execute_script("arguments[0].click();", element)
            else:
                raise