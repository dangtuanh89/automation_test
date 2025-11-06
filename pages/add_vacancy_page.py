from base.base_page import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
import time

class AddVacancyPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.add_vacancy =(By.XPATH, "//h6[text()='Add Vacancy']")
        self.vacancy_name_field = (By.XPATH, "//label[text()='Vacancy Name']/following::input[@class='oxd-input oxd-input--active'][1]")
        self.job_title_select_box = (By.XPATH, "//label[text()='Job Title']/following::div[@class='oxd-select-text-input']")
        self.automation_tester = (By.XPATH, "//div[@role='listbox']//div[@role='option']//span[normalize-space()='Automaton Tester']")
        self.description_field = (By.XPATH, "//textarea[@placeholder='Type description here']")
        self.hiring_manager_field = (By.XPATH, "//input[@placeholder='Type for hints...']")
        self.number_of_positions = (By.XPATH, "//label[text()='Number of Positions']/following::input[@class='oxd-input oxd-input--active']")
        self.current_login_user = (By.XPATH, "//p[@class='oxd-userdropdown-name']")
        self.active = (By.XPATH, "//p[text()='Active']/following-sibling::div//span[contains(@class, 'oxd-switch-input')]")
        self.publish = (By.XPATH, "//p[text()='Publish in RSS Feed and Web Page']/following-sibling::div//span[contains(@class, 'oxd-switch-input')]")
        self.save_btn = (By.XPATH, "//button[text()=' Save ']")
        self.vacancies = (By.XPATH, "//h5[text()='Vacancies']")
        self.automation_tester_vacancies_page = (By.XPATH, "//div[@role='option']//span[normalize-space()='Automaton Tester']")
        
        self.job_title_field_path = (By.XPATH, "//label[text()='Job Title']/following::div[@class='oxd-select-text-input'][1]")       
        self.job_title_options_path =(By.XPATH, "//div[@role='listbox']//div[@role='option']//span")
        self.vacancy_field_path = (By.XPATH, "//label[text()='Vacancy']/following::div[@class='oxd-select-text-input'][1]")
        self.vacancy_options_path = self.job_title_options_path     
        self.hiring_manager_field_path = (By.XPATH, "//label[text()='Hiring Manager']/following::div[@class='oxd-select-text-input'][1]")
        self.hiring_manager_options_path = self.job_title_options_path
        self.status_field_path = (By.XPATH, "//label[text()='Status']/following::div[@class='oxd-select-text-input']")
        self.status_options_path = self.job_title_options_path
        self.dropdown_xpath = (By.XPATH, "//div[@role='listbox']")
        self.search_btn = (By.XPATH, "//button[text()=' Search ']")
        self.search_results = (By.XPATH, "//div[@role='table']//div[@role='rowgroup']//div[@role='row'][.//div[@role='cell']]")
        self.record_cells = (By.XPATH, ".//div[@role='cell']")
        self.search_btn = (By.XPATH, "//button[text()=' Search ']")
        self.reset_btn = (By.XPATH, "//button[text()=' Reset ']")
    
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
    
    def click_search_btn(self):
        self.get_element(self.search_btn).click()

    def click_reset_btn(self):
        self.get_element(self.reset_btn).click()
    
    def verify_vacancies_displayed(self):
        return self.is_displayed(self.vacancies)
    
    def wait_for_vacancies_page(self):
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//h5[text()='Vacancies']")))

    def search_job(self):
        self.wait_for_vacancies_page()
        dropdown_xpath = "//div[@role='listbox']"
        for attempt in range(3):
            self.wait_and_click(self.job_title_vacancies_page)
            try:
                WebDriverWait(self.driver, 5).until(EC.visibility_of_element_located((By.XPATH, dropdown_xpath)))
                break
            except:
                print(f"Attempt {attempt + 1}: Dropdown not opened, retrying...")
                if attempt == 2:
                    raise Exception("Job Title dropdown could not be opened after multiple attempts")

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
        expected_job_title = "Automaton Tester"
        expected_hiring_manager = self.get_element(self.current_login_user).text
        rows = self.get_elements(self.search_results)
        if not rows:
            print("No search record found")
            return False
        
        # Variable to check if newly created record is found
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

    def verify_search_records_by_text(self, expected_value, filter_name):
        try:
            WebDriverWait(self.driver, 10).until(EC.presence_of_all_elements_located(self.search_results))
            rows = self.get_elements(self.search_results)
        except TimeoutException:
            print(f"No search records found for {filter_name} '{expected_value}' — but filter works correctly (empty result).")
            return True
        
        if not rows:
            print(f"No search records found for {filter_name} '{expected_value}' — but filter works correctly (empty result).")
            return True
        
        for row in rows:
            cells = row.find_elements(*self.record_cells)
            cell_texts = [cell.text.strip() for cell in cells]
            row_content = " ".join(cell_texts)

            if expected_value.lower() not in row_content.lower():
                print(f"Records found : {'|'.join(cell_texts)} does not contain filter value: {expected_value}")
                return False
        
        print(f"All search records match with filter value: {expected_value}")
        return True

    def _run_single_filter_verification_loop(self, field_locator, options_locator, filter_name):
        print(f"\n--- Collect options for {filter_name} ---")
        self.wait_and_click(field_locator)
        options_elements = self.get_elements(options_locator)
        options = [element.text.strip() for element in options_elements]
        ActionChains(self.driver).send_keys(Keys.ESCAPE).perform()
        print(f"Collected {filter_name} options: {options}")

        failed_options = []
        for option_value in options:
            print(f"\n-- Testing filter for {filter_name}: {option_value}")
            try:
                self.select_dropdown_value(field_locator, option_value)
                self.click_search_btn()
                if not self.verify_search_records_by_text(expected_value=option_value, filter_name=filter_name):
                    failed_options.append(option_value)
            except Exception as e:
                # Bắt lỗi nếu không thể chọn hoặc tìm kiếm thất bại
                print(f"Unexpected error during test for {filter_name} '{option_value}': {e}")
                failed_options.append(option_value)
                
            finally:
                # 5. Đặt lại bộ lọc và chờ field có thể click lại
                self.click_reset_btn()
                WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable(field_locator)) 
                
        return failed_options

    def verify_filter_vacancies_based_job_title(self):
        failed = self._run_single_filter_verification_loop(field_locator=self.job_title_field_path, options_locator=self.job_title_options_path, filter_name="Job Title")
        if failed:
            print(f"\n Some Job Title options failed verification: {failed}")
            return False
        print("\n All Job Title filters verified successfully!")
        return True
    
    def verify_filter_vacancies_based_on_hiring_manager(self):
        failed = self._run_single_filter_verification_loop(field_locator=self.hiring_manager_field_path, options_locator=self.hiring_manager_options_path, filter_name="Hiring Manager")
        if failed:
            print(f"\n Some Hiring Manager options failed verification: {failed}")
            return False
        print("\n All Hiring Manager filters verified successfully!")
        return True
    
    def verify_filter_vacancies_based_on_status(self):
        failed = self._run_single_filter_verification_loop(field_locator=self.status_field_path, options_locator=self.status_options_path, filter_name="Status")
        if failed:
            print(f"\n Some Status options failed verification: {failed}")
            return False
        print("\n All Status filters verified successfully!")
        return True
    
    def verify_filter_vacancies_based_on_vacancy(self):
        failed = self._run_single_filter_verification_loop(field_locator=self.vacancy_field_path, options_locator=self.vacancy_options_path, filter_name="Vacancy")
        if failed:
            print(f"\n Some Vacancy options failed verification: {failed}")
            return False
        print("\n All Vacancy filters verified successfully!")
        return True

    def verify_search_records_based_on_4_filters_by_text(self, expected_job_title, expected_vacancy, expected_hiring_manager, expected_status):
        rows = self.get_elements(self.search_results)
        if not rows:
            print(f"No search records found but filter works correctly (empty result).")
            return True
        
        for row in rows:
            cells = row.find_elements(*self.record_cells)
            cell_text =[cell.text.strip() for cell in cells]
            row_content = " ".join(cell_text)

            if expected_job_title.lower() not in row_content.lower() or expected_vacancy.lower() not in row_content.lower() or expected_hiring_manager.lower() not in row_content.lower() or expected_status.lower() not in row_content.lower():
                print(f"Records found: {'|'.join(cell_text)} does not containsome or all filters")
                return False
        
        print(f"All records match with filters")
        return True

    def verify_filter_vacancies_by_4_filters(self, job_title, vacancy, hiring_manager, status):
        self.select_dropdown_value(self.job_title_field_path, job_title)
        self.select_dropdown_value(self.vacancy_field_path, vacancy)
        self.select_dropdown_value(self.hiring_manager_field_path, hiring_manager)
        self.select_dropdown_value(self.status_field_path, status)

        self.get_element(self.search_btn).click()

        if not self.verify_search_records_based_on_4_filters_by_text(expected_job_title=job_title, expected_vacancy=vacancy, expected_hiring_manager=hiring_manager, expected_status=status):
            print("Verification failed for filters")
            return False
        else:
            print("All filters verified successfully")
            return True

        




        


