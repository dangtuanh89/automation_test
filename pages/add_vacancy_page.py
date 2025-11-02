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
        self.job_title_vacancies_page = (By.XPATH, "//label[text()='Job Title']/following::div[@class='oxd-select-text-input'][1]")
        self.job_title_options = (By.XPATH, "//div[@role='listbox']//div[@role='option']//span")
        self.automation_tester_vacancies_page = (By.XPATH, "//div[@role='option']//span[normalize-space()='Automaton Tester']")
        self.hiring_manager_vacancies_page = (By.XPATH, "//label[text()='Hiring Manager']/following::div[@class='oxd-select-text-input'][1]")
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
    
    def wait_for_vacancies_page(self, timeout=10):
        WebDriverWait(self.driver, timeout).until(
        EC.visibility_of_element_located((By.XPATH, "//h5[text()='Vacancies']")))

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

    def verify_search_records_based_on_vacancy_by_text(self, expected_vacancy):
        try:
            WebDriverWait(self.driver, 10).until(EC.presence_of_all_elements_located(self.search_results))
            rows = self.get_elements(self.search_results)
        except TimeoutException:
            print(f"No search records found for vacancy: {expected_vacancy}")
            return False
        
        if not rows:
            print("No search records found")
            return False
        
        for row in rows:
            cells = row.find_elements(*self.record_cells)
            cell_texts = [cell.text.strip() for cell in cells]
            row_content = " ".join(cell_texts)

            if expected_vacancy.lower() not in row_content.lower():
                print(f"Records found : {'|'.join(cell_texts)} does not contain filter value: {expected_vacancy}")
                return False
        
        print(f"All search records match with filter value: {expected_vacancy}")
        return True

    def verify_filter_vacancies_based_on_vacancy(self):
        vacancy_field_path = (By.XPATH, "//label[text()='Vacancy']/following::div[@class='oxd-select-text-input'][1]")
        vacancy_dropdown_path = (By.XPATH, "//div[@role='listbox']")
        vacancy_options_path = (By.XPATH, "//div[@role='listbox']//div[@role='option']//span")

        self.get_element(vacancy_field_path).click()
        vacancy_options_elements = self.get_elements(vacancy_options_path)
        vacancy_options = [element.text.strip() for element in vacancy_options_elements]
        ActionChains(self.driver).send_keys(Keys.ESCAPE).perform()
        print(f"Collected vacancy options: {vacancy_options}")

        failed_vacancy_options = []

        for vacancy in vacancy_options:
            print(f"\n-- Testing filter for vacancy option: {vacancy}")
            for attempt in range(3):
                try:
                    self.get_element(vacancy_field_path).click()
                    WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(vacancy_dropdown_path))
                    break
                except (TimeoutException, StaleElementReferenceException):
                    print(f"Attempt {attempt + 1}/3: Dropdown not ready for '{vacancy}', retrying...")
                    ActionChains(self.driver).send_keys(Keys.ESCAPE).perform()
                    time.sleep(1)
                    if attempt == 2:
                        print(f"Skipping '{vacancy}' (dropdown failed to open after retry)")
                        failed_vacancy_options.append(vacancy)
                        continue # Skip this vacancy
                
            if vacancy in failed_vacancy_options:
                continue

            specific_vacancy = (By.XPATH, f"//div[@role='listbox']//div[@role='option']//span[normalize-space() = '{vacancy}']")
            
            self.get_element(specific_vacancy).click()
            self.get_element(self.search_btn).click()

            if not self.verify_search_records_based_on_vacancy_by_text(expected_vacancy=vacancy):
                print(f"Verification failed for vacancy option: {vacancy}")
                failed_vacancy_options.append(vacancy)
            else:
                print(f"Verified successfully for: {vacancy}")

            self.click_reset_btn()
            WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable(vacancy_field_path)) 
        
        if failed_vacancy_options:
            print(f"\n Some vacancy options failed verification: {failed_vacancy_options}")
            return False
        else:
            print("\n All vacancy filters verified successfully!")
            return True

    def verify_search_record_based_on_job_title_by_text(self, expected_job_title):
        try:
            WebDriverWait(self.driver, 10).until(EC.presence_of_all_elements_located(self.search_results))
            rows = self.get_elements(self.search_results)
        except TimeoutException:
            print(f'No search record found for job title: {expected_job_title}')
            return False
            
        if not rows:
            print("No search records found")
            return False
        
        for row in rows:
            cells = row.find_elements(*self.record_cells)
            cell_text = [cell.text.strip() for cell in cells]
            row_content = " ".join(cell_text)

            if expected_job_title.lower() not in row_content.lower():
                print(f"Records found: {'|'.join(cell_text)} does not contain {expected_job_title}")
                return False
            
        print(f"All records match with filter value: {expected_job_title}")
        return True
             
    def verify_filter_vacancies_based_job_title(self):
        job_title_field_path = (By.XPATH, "//label[text()='Job Title']/following::div[@class='oxd-select-text-input'][1]")
        job_title_dropdown_path = (By.XPATH, "//div[@role='listbox']")
        job_title_options_path =(By.XPATH, "//div[@role='listbox']//div[@role='option']//span")

        self.get_element(job_title_field_path).click()
        job_title_elements = self.get_elements(job_title_options_path)
        job_title_options = [element.text.strip() for element in job_title_elements]
        ActionChains(self.driver).send_keys(Keys.ESCAPE).perform()
        print(f"Collected job title options: {job_title_options}")

        failed_job_titles = []

        for job_title in job_title_options:
            print(f"\n --Testing filter for job title: {job_title}")
            for attempt in range(3):
                try:
                    self.get_element(job_title_field_path).click()
                    WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(job_title_dropdown_path))
                    break
                except (TimeoutException, StaleElementReferenceException):
                    print(f"Attempt {attempt + 1}/3: Dropdown not ready for job title {job_title}, retrying...")
                    ActionChains(self.driver).send_keys(Keys.ESCAPE).perform()
                    time.sleep(1)
                    if attempt == 2:
                        print(f"Skipping '{job_title}', dropdown failed to open after retries")
                        failed_job_titles.append(job_title)
                        continue

            if job_title in failed_job_titles:
                continue

            specific_job_title = (By.XPATH, f"//div[@role='listbox']//div[@role='option']//span[normalize-space() = '{job_title}']")
            self.get_element(specific_job_title).click()

            self.click_search_btn()

            if not self.verify_search_record_based_on_job_title_by_text(expected_job_title = job_title):
                print(f"Verification failed for job title: {job_title}")
                failed_job_titles.append(job_title)
            else:
                print(f"Verified successfully for job title: {job_title}")
            
            self.click_reset_btn()
            WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(job_title_field_path))

        if failed_job_titles:
            print(f"\n Some job tiles failed for verification: {failed_job_titles}")
            return False
        else:
            print("\n All job titles verified successfully")
            return True
        
    def verify_search_records_based_on_hiring_manager_by_text(self, expected_hiring_manager):
        try:
            WebDriverWait(self.driver, 10).until(EC.presence_of_all_elements_located(self.search_results))
            rows = self.get_elements(self.search_results)
        except TimeoutException:
            print(f"No search records found for hiring manager: {expected_hiring_manager}")
            return False
        
        if not rows:
            print('No search records found')
            return False
        
        for row in rows:
            cells = row.find_elements(*self.record_cells)
            cell_text = [cell.text.strip() for cell in cells]
            row_content = " ".join(cell_text)

            if expected_hiring_manager.lower() not in row_content.lower():
                print(f'Records found: {'|'.join(cell_text)} does not contain hiring manager: {expected_hiring_manager}')
                return False
        
        print(f"All records match with filter value: {expected_hiring_manager}")
        return True

    def verify_filter_vacancies_based_on_hiring_manager(self):
        hiring_manager_field_path = (By.XPATH, "//label[text()='Hiring Manager']/following::div[@class='oxd-select-text-input'][1]")
        hiring_manager_dropdown_path = (By.XPATH, "//div[@role='listbox']")
        hiring_manager_options_path = (By.XPATH, "//div[@role='listbox']//div[@role='option']//span")

        self.get_element(hiring_manager_field_path).click()
        hiring_manager_elements = self.get_elements(hiring_manager_options_path)
        hiring_manager_options = [element.text.strip() for element in hiring_manager_elements]
        ActionChains(self.driver).send_keys(Keys.ESCAPE).perform()
        print(f"Collected hiring manager options: {hiring_manager_options}")

        failed_hiring_manager_options = []

        for hiring_manager in hiring_manager_options:
            print(f"\n-- Testing filter for hiring manger: {hiring_manager}")
            for attempt in range(3):
                try:
                    self.get_element(hiring_manager_field_path).click()
                    WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(hiring_manager_dropdown_path))
                    break
                except (TimeoutException, StaleElementReferenceException):
                    print(f"Attempt {attempt + 1}/3: Dropdown not ready for hiring manager '{hiring_manager}', retrying...")
                    ActionChains(self.driver).send_keys(Keys.ESCAPE).perform()
                    time.sleep(1)
                    if attempt == 2:
                        print(f"Skipping '{hiring_manager}', dropdown failed to open after retries")
                        failed_hiring_manager_options.append(hiring_manager)
                        continue

            if hiring_manager in failed_hiring_manager_options:
                    continue

            specific_hiring_manager = (By.XPATH, f"//div[@role='listbox']//div[@role='option']//span[normalize-space() = '{hiring_manager}']")
            self.get_element(specific_hiring_manager).click()
            self.click_search_btn()

            if not self.verify_search_records_based_on_hiring_manager_by_text(expected_hiring_manager=hiring_manager):
                print(f"Verification failed for hiring manager: {hiring_manager}")
                failed_hiring_manager_options.append(hiring_manager)
            else:
                print(f"Verified successfully for hiring manager: {hiring_manager}")
            
            self.click_reset_btn()
            WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(hiring_manager_field_path))

        if failed_hiring_manager_options:
            print(f"\n Some hiring manager options for verification: {failed_hiring_manager_options}")
            return False
        else:
            print(f"\n All hiring manager options verified successfully")
            return True    


  