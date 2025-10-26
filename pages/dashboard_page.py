from selenium.webdriver.common.by import By
from base.base_page import BasePage

class DashboardPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.dashboard = (By.XPATH, "//h6[@class='oxd-text oxd-text--h6 oxd-topbar-header-breadcrumb-module']")
        self.recruitment_menu = (By.XPATH, "//span[text()='Recruitment']")
        self.user_profile = (By.XPATH, "//p[@class='oxd-userdropdown-name']")
        self.logout_btn = (By.XPATH, "//a[text()='Logout']")

    def is_dashboard_displayed(self):
        return self.is_displayed(self.dashboard)
    
    def is_recruitment_displayed(self):
        return self.is_displayed(self.recruitment_menu)
    
    def logout(self):
        self.get_element(self.user_profile).click()
        self.get_element(self.logout_btn).click()
    
    def click_recruitment_menu(self):
        self.get_element(self.recruitment_menu).click()