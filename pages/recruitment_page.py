from base.base_page import BasePage
from selenium.webdriver.common.by import By

class RecruitmentPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.vacancies_tab = (By.XPATH, "//a[text()='Vacancies']")
        self.add_btn = (By.XPATH, "//button[text()=' Add ']")

    def click_vacancies_tab(self):
        self.get_element(self.vacancies_tab).click()
        
    def click_add_btn(self):
        self.get_element(self.add_btn).click()

    

