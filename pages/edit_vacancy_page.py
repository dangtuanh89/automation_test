from base.base_page import BasePage
from selenium.webdriver.common.by import By

class EditVacancyPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.edit_vacancy = (By.XPATH, "//h6[text()='Edit Vacancy']")
        self.cancel_btn = (By.XPATH, "//button[text()=' Cancel ']")
    
    def verify_edit_vacancy_displayed(self):
        return self.is_displayed(self.edit_vacancy)
    
    def click_cancel_btn(self):
        self.get_element(self.cancel_btn).click()