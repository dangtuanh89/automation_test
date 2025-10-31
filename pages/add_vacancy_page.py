from base.base_page import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class AddVacancyPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.add_vacancy =(By.XPATH, "//h6[text()='Add Vacancy']")
        self.vacancy_name_field = (By.XPATH, "//label[text()='Vacancy Name']/following::input[@class='oxd-input oxd-input--active'][1]")
        self.job_title_select_box = (By.XPATH, "//label[text()='Job Title']/following::div[@class='oxd-select-text-input']")
        self.automation_tester = (By.XPATH, "//div[@role='listbox']//div[@role='option']//span[text()='Automation Tester']")
        self.description_field = (By.XPATH, "//textarea[@placeholder='Type description here']")
        self.hiring_manager_field = (By.XPATH, "//input[@placeholder='Type for hints...']")
        self.number_of_positions = (By.XPATH, "//label[text()='Number of Positions']/following::input[@class='oxd-input oxd-input--active']")
        self.current_login_user = (By.XPATH, "//p[@class='oxd-userdropdown-name']")
        self.active = (By.XPATH, "//p[text()='Active']/following-sibling::div//span[contains(@class, 'oxd-switch-input')]")
        self.publish = (By.XPATH, "//p[text()='Publish in RSS Feed and Web Page']/following-sibling::div//span[contains(@class, 'oxd-switch-input')]")
        self.save_btn = (By.XPATH, "//button[text()=' Save ']")
        self.vacancies = (By.XPATH, "//h5[text()='Vacancies']")
        self.job_title_vacancies_page = (By.XPATH, "//label[text()='Job Title']/following::div[@class='oxd-select-text-input'][1]")
        self.automation_tester_vacancies_page = (By.XPATH, "//div[@role='option']//span[text()='Automation Tester']")
        self.hiring_manager_vacancies_page = (By.XPATH, "//label[text()='Hiring Manager']/following::div[@class='oxd-select-text-input'][1]")
        self.search_btn = (By.XPATH, "//button[text()=' Search ']")
        self.search_results = (By.XPATH, "//div[@role='table']//div[@role='row'][.//div[@role='cell']]")
        self.record_cells = (By.XPATH, ".//div[@role='cell']")

    def verify_add_vacancy_displayed(self):
        return self.is_displayed(self.add_vacancy)
    
    def input_vacancy_data(self, vacancy_name, description, number_of_position):
        self.type(self.vacancy_name_field, vacancy_name)
        self.wait_and_click(self.job_title_select_box)
        self.wait_and_click(self.automation_tester)
        self.type(self.description_field, description)
        self.type(self.number_of_positions, number_of_position)

    def choose_hiring_manager(self):
        current_login_user = self.get_element(self.current_login_user).text
        self.type(self.hiring_manager_field, current_login_user)
        suggestion = (By.XPATH, f"//div[@role='listbox']//span[contains(., '{current_login_user.split()[0]}')]")
        self.wait_and_click(suggestion)
        
    def is_active_selected(self):
        active = self.get_element(self.active)
        return "oxd-switch-input--active" in active.get_attribute("class")

    def set_active_to_false(self):
        if self.is_active_selected():
            self.click_by_js(self.active)
    
    def is_publish_selected(self):
        publish = self.get_element(self.publish)
        return "oxd-switch-input--active" in publish.get_attribute("class")
    
    def set_publish_to_true(self):
        if not self.is_publish_selected():
            self.click_by_js(self.publish)
    
    def click_save_btn(self):
        self.get_element(self.save_btn).click()
    
    def verify_vacancies_displayed(self):
        return self.is_displayed(self.vacancies)

    def search_job(self):
        self.wait_and_click(self.job_title_vacancies_page)
        WebDriverWait(self.driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//div[@role='listbox']"))
    )
        self.wait_and_click(self.automation_tester_vacancies_page)
        current_login_user = self.get_element(self.current_login_user).text
        self.wait_and_click(self.hiring_manager_vacancies_page)
        hiring_manager = (By.XPATH, f"//div[@role='listbox']//span[contains(., '{current_login_user.split()[0]}')]")
        self.wait_and_click(hiring_manager)
        self.wait_and_click(self.search_btn)

    def verify_has_search_record(self):
        rows = self.get_elements(self.search_results)
        if rows:
            print("There is at least one search record that exists")
            return True
        else:
            print('No search record found')
            return False
    
    def verify_search_data(self):
        expected_job_title = "Automation Tester"
        expected_hiring_manager = self.get_element(self.current_login_user).text
        rows = self.get_elements(self.search_results)
        if not rows:
            print("No search record found")
            return False
        
        # Biến để kiểm tra xem bản ghi mới tạo có được tìm thấy không
        found_matching_record = False
        for row in rows:
            cells = row.find_elements(*self.record_cells)
            print([cell.text.strip() for cell in cells])
            try:
                actual_job_title = cells[2].text.strip()
                actual_hiring_manager = cells[3].text.strip()
            except IndexError:
                continue

            if actual_job_title == expected_job_title and expected_hiring_manager in actual_hiring_manager:
                found_matching_record = True
                print(f"Found matching record with correct Job Title: {actual_job_title} and Hiring Manager: {actual_hiring_manager}.")
                return True
            
        if not found_matching_record:
            print(f"No matching record found with the expected Job Title: {actual_job_title} and Hiring Manager {actual_hiring_manager}.")
            return False
       





