from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException 
import time
import os

class BasePage:
    def __init__(self, driver):
        self.driver = driver

    def get_element(self, locator):
        element = WebDriverWait(self.driver, 15).until(EC.presence_of_element_located(locator))
        return element
    
    def get_elements(self, locator):
        elements = WebDriverWait(self.driver, 15).until(EC.presence_of_all_elements_located(locator))
        return elements
    
    def type(self, locator, text):
        element = WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable(locator))
        element.clear()
        element.send_keys(text)

    def is_displayed(self, locator):
        element = WebDriverWait(self.driver, 15).until(EC.presence_of_element_located(locator))
        return element.is_displayed()

    def click_by_js(self, locator):
        element = WebDriverWait(self.driver, 15).until(EC.presence_of_element_located(locator))
        self.driver.execute_script("arguments[0].click();", element)

    def wait_and_click(self, locator, use_js_fallback: bool = True, timeout: int = 20, retries: int = 3):
        """
        Click vào phần tử an toàn với retry, scroll và JS fallback.
        Dùng cho dropdown hoặc nút có thể bị che, load chậm, hoặc DOM thay đổi.
        """

        # Biến dùng để lưu lại lỗi cuối cùng xảy ra (nếu tất cả lần click đều thất bại)
        last_exception = None

        # Thử click nhiều lần (theo số lần 'retries')
        for attempt in range(retries):
            try:
                # Chờ phần tử có thể click được
                element = WebDriverWait(self.driver, timeout).until(EC.element_to_be_clickable(locator))

                # Cuộn phần tử vào giữa màn hình (phòng khi bị khuất)
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)

                # Thực hiện click
                element.click()
                return  # Thành công -> thoát hàm

            except Exception as e:
                # Nếu click thất bại, lưu lại lỗi và thử lại
                last_exception = e
                print(f"Attempt {attempt + 1} failed to click element {locator}: {e}")
                time.sleep(1)  # Chờ 1s rồi thử lại

        # Nếu đã thử đủ 'retries' lần mà vẫn lỗi, thì thử click bằng JavaScript fallback
        if use_js_fallback:
            try:
                element = WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located(locator))
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
                self.driver.execute_script("arguments[0].click();", element)
                print(f"Clicked {locator} via JS fallback.")
                return  # Click thành công bằng JS
            except Exception as e:
                # Nếu JS click cũng lỗi, ghi nhận lỗi cuối cùng
                last_exception = e

        # Nếu vẫn không click được, chụp screenshot để debug
        screenshot_dir = os.getenv("SCREENSHOT_DIR", "screenshots")
        os.makedirs(screenshot_dir, exist_ok=True)
        filename = os.path.join(screenshot_dir, f"click_error_{int(time.time())}.png")
        self.driver.save_screenshot(filename)
        print(f"Click failed on {locator}, screenshot saved to: {filename}")

        # Ném lại lỗi cuối cùng (giúp traceback chính xác)
        raise last_exception
    
    def open_dropdown(self, locator, listbox_xpath="//div[@role='listbox']", retries=3):
        for attempt in range(retries):
            self.get_element(locator).click()
            try:
                WebDriverWait(self.driver, 3).until(EC.presence_of_element_located((By.XPATH, listbox_xpath)))
                return
            except:
                print(f"Attempt {attempt + 1}: dropdown not opened, retrying...")
        raise TimeoutException("Dropdown could not be opened after multiple attempts")