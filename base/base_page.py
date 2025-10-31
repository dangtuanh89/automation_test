from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os

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
        element = WebDriverWait(self.driver, 15).until(EC.presence_of_element_located(locator))
        self.driver.execute_script("arguments[0].click();", element)

    def wait_and_click(self, locator, use_js_fallback: bool = True, timeout: int = 20, retries: int = 2):
        for attempt in range (retries +1):
            try:
                element = WebDriverWait(self.driver, timeout).until(EC.element_to_be_clickable(locator))
                element.click()
                return
            except Exception as e:
                if attempt < retries:
                    time.sleep(1)
                else:
                    try:
                        if use_js_fallback:
                            element = WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located(locator))
                            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
                            self.driver.execute_script("arguments[0].click();", element)
                        else:
                            raise e
                    except Exception as final_e:
                        screenshot_dir = os.getenv("SCREENSHOT_DIR", "screenshots")
                        os.makedirs(screenshot_dir, exist_ok=True)
                        filename = os.path.join(
                            screenshot_dir,f"wait_and_click_error_{int(time.time())}.png")
                        self.driver.save_screenshot(filename)
                        print(f"Click failed, screenshot saved to: {filename}")
                        raise final_e