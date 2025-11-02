from base.base_test import BaseTest
from utils.config_reader import ConfigReader
import pytest

class TestAddVacancy(BaseTest):
    @pytest.mark.smoke
    def test_add_new_automation_tester_vacancy(self, login_page, dashboard_page, recruitment_page, add_vacancy_page, edit_vacancy_page):
        login_page.login(ConfigReader.get_username(), ConfigReader.get_password())
        dashboard_page.click_recruitment_menu()
        recruitment_page.click_vacancies_tab()
        recruitment_page.click_add_btn()
        assert add_vacancy_page.verify_add_vacancy_displayed(), "Add vacancy page is not displayed"
        print("Add vacancy page is displayed")
        #add_vacancy_page.input_vacancy_data(ConfigReader.get_vacancy_name(), ConfigReader.get_description, ConfigReader.get_number_of_positions)
        add_vacancy_page.input_vacancy_data(ConfigReader.get_vacancy_name(), ConfigReader.get_description(), ConfigReader.get_number_of_positions())
        add_vacancy_page.choose_hiring_manager()
        add_vacancy_page.set_active_to_false()
        add_vacancy_page.set_publish_to_true()
        add_vacancy_page.click_save_btn()
        assert edit_vacancy_page.verify_edit_vacancy_displayed(), "Edit vacancy page is not displayed"
        print("Edit vacancy page is displayed")
        edit_vacancy_page.click_cancel_btn()
        assert add_vacancy_page.verify_vacancies_displayed(), "Vacancies page is not displayed again after click cancel"
        print("Vacancies page is displayed again after click cancel")
        add_vacancy_page.search_job()
        assert add_vacancy_page.verify_has_search_record(), "No search record found"
        assert add_vacancy_page.verify_search_data(), "Search results data mismatch with input criteria"

    def test_filter_vacancies_based_on_job_title(self, login_page, dashboard_page, recruitment_page, add_vacancy_page):
        login_page.login(ConfigReader.get_username(), ConfigReader.get_password())
        dashboard_page.click_recruitment_menu()
        recruitment_page.click_vacancies_tab()
        assert add_vacancy_page.verify_filter_vacancies_based_job_title(), "The returned records does not match with the filter"

    def test_filter_vacancies_based_on_vacancy(self, login_page, dashboard_page, recruitment_page, add_vacancy_page):
        login_page.login(ConfigReader.get_username(), ConfigReader.get_password())
        dashboard_page.click_recruitment_menu()
        recruitment_page.click_vacancies_tab()
        assert add_vacancy_page.verify_filter_vacancies_based_on_vacancy(), "The returned records does not match with vacancy filter"
    
    def test_filter_vacancies_based_on_hiring_manager(self, login_page, dashboard_page, recruitment_page, add_vacancy_page):
        login_page.login(ConfigReader.get_username(), ConfigReader.get_password())
        dashboard_page.click_recruitment_menu()
        recruitment_page.click_vacancies_tab()
        assert add_vacancy_page.verify_filter_vacancies_based_on_hiring_manager(), "The returned records does not match with hiring manager filter"
        
