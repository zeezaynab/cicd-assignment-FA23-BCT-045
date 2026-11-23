import os
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

URL = os.getenv("BASE_URL", "http://localhost:8081")


@pytest.fixture
def driver():
    o = Options()
    o.binary_location = "/usr/bin/chromium"
    for a in ["--headless=new", "--no-sandbox", "--disable-dev-shm-usage"]:
        o.add_argument(a)
    d = webdriver.Chrome(service=Service("/usr/bin/chromedriver"), options=o)
    yield d
    d.quit()


def test_title(driver):
    driver.get(URL)
    assert "CI/CD Assignment" in driver.title


def test_heading(driver):
    driver.get(URL)
    assert "FA23" in driver.find_element(By.ID, "heading").text


def test_button_click(driver):
    driver.get(URL)
    driver.find_element(By.ID, "submit-btn").click()
    assert "You entered" in driver.find_element(By.ID, "output").text


def test_text_input(driver):
    driver.get(URL)
    driver.find_element(By.ID, "textbox").send_keys("hello")
    driver.find_element(By.ID, "submit-btn").click()
    assert "hello" in driver.find_element(By.ID, "output").text
    os.makedirs("shots", exist_ok=True)
    driver.save_screenshot("shots/test_run.png")