import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# This is our test data: each tuple is (username, password, expected_result)
test_data = [
    ("standard_user", "secret_sauce", "success"),
    ("standard_user", "wrong_password", "error"),
    ("locked_out_user", "secret_sauce", "error"),
    ("", "", "error"),
]

@pytest.mark.parametrize("username, password, expected", test_data)
def test_login(username, password, expected):
    driver = webdriver.Chrome()
    driver.get("https://www.saucedemo.com/")

    driver.find_element(By.ID, "user-name").send_keys(username)
    driver.find_element(By.ID, "password").send_keys(password)
    driver.find_element(By.ID, "login-button").click()

    wait = WebDriverWait(driver, 5)

    if expected == "success":
        # Should land on products page
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "inventory_list")))
        assert True
    else:
        # Should show an error message
        error = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "h3[data-test='error']")))
        assert error.is_displayed()

    driver.quit()