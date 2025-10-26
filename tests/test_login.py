from base.base_test import BaseTest
from utils.config_reader import ConfigReader


class TestLoginPage(BaseTest):
    def test_login_sucessful(self, login_page, dashboard_page):
        assert login_page.verify_username_field_is_displayed(), "Username field is not displayed"
        assert login_page.verify_password_field_is_displayed(), "Password field is not displayed"
        login_page.login(ConfigReader.get_username(), ConfigReader.get_password())
        assert dashboard_page.is_dashboard_displayed(), "Dashboard page is not displayed"
        print("Navigated to Dashboard page successful")
        assert dashboard_page.is_recruitment_displayed(), "Recruitment menu is not displayed"
        print("Recruitment menu is displayed")
        dashboard_page.logout()
        assert login_page.verify_username_field_is_displayed(), "Login page is not displayed after logout"
        print("Login page is displayed after logout")

    def test_login_failed(self, login_page, dashboard_page):
        assert login_page.verify_username_field_is_displayed(), "Username field is not displayed"
        assert login_page.verify_password_field_is_displayed(), "Password field is not displayed"
        login_page.click_login_btn()
        assert login_page.verify_require_username_displayed(), "Required error for username is not displayed"
        assert login_page.verify_require_password_displayed(), "Required error for password is not displayed"
        login_page.login(ConfigReader.get_invalid_username(), ConfigReader.get_invalid_password())
        assert login_page.vefiry_invalid_credentials_displayed(), "Invalid credentials message is not displayed"
        login_page.login(ConfigReader.get_username(), ConfigReader.get_password())
        assert dashboard_page.is_dashboard_displayed(), "Dashboard page is not displayed"
        dashboard_page.logout()

        
        