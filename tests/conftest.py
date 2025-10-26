from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from pages.recruitment_page import RecruitmentPage
from pages.add_vacancy_page import AddVacancyPage
from pages.edit_vacancy_page import EditVacancyPage
import pytest

@pytest.fixture(scope= "class")
def login_page(request):
    login_page = LoginPage(request.cls.driver)
    return login_page

@pytest.fixture(scope= "class")
def dashboard_page(request):
    dashboard_page = DashboardPage(request.cls.driver)
    return dashboard_page

@pytest.fixture(scope= "class")
def recruitment_page(request):
    recruitment_page = RecruitmentPage(request.cls.driver)
    return recruitment_page

@pytest.fixture(scope= "class")
def add_vacancy_page(request):
    add_vacancy_page = AddVacancyPage(request.cls.driver)
    return add_vacancy_page

@pytest.fixture(scope= "class")
def edit_vacancy_page(request):
    edit_vacancy_page = EditVacancyPage(request.cls.driver)
    return edit_vacancy_page