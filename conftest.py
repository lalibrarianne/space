import pytest

from pages.base_page import BasePage
from pages.space_page import SpacePage

@pytest.fixture
def base_page(page) -> BasePage:
    return BasePage(page)

@pytest.fixture
def space_page(page) -> SpacePage: 
    return SpacePage(page)

pytest_plugins = ("fixtures.browsers")
