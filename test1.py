import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import os

class LoginTest(unittest.TestCase):

    def setUp(self):
        # Create a WebDriver instance
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()

    def tearDown(self):
        # Close the browser
        self.driver.quit()

    def save_screenshot(self, name):
        # Create the screenshots directory if it doesn't exist
        if not os.path.exists('screenshots'):
            os.makedirs('screenshots')

        # Capture and save the screenshot
        self.driver.save_screenshot(f'screenshots/{name}.png')

    def test_login_success(self):
        # Open the desired URL
        self.driver.get("http://localhost:3000/start")

        # Find and click the login button
        admin = self.driver.find_element(By.XPATH, "/html/body/div/div/div/div[2]/div/button[2]")
        admin.click()

        # Fill in the login form
        admin_uname = self.driver.find_element(By.XPATH, "/html/body/div/div/div/form/div[1]/input")
        admin_pwd = self.driver.find_element(By.XPATH, "/html/body/div/div/div/form/div[2]/input")
        admin_submit = self.driver.find_element(By.XPATH, "/html/body/div/div/div/form/button")

        admin_uname.send_keys("admin@gmail.com")
        admin_pwd.send_keys("admin")
        admin_submit.click()

        # Explicitly wait for the welcome message element to be visible
        welcome_message = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "/html/body/div/div/div/div[1]/div/a/span"))
        ).text

        # Assert that the login was successful
        self.assertEqual(welcome_message, "Admin Dashboard")

        # Save a screenshot
        self.save_screenshot("login_success")

    def test_login_failure(self):
        # Open the desired URL
        self.driver.get("http://localhost:3000/start")

        # Find and click the login button
        admin = self.driver.find_element(By.XPATH, "/html/body/div/div/div/div[2]/div/button[2]")
        admin.click()

        # Fill in the login form with incorrect credentials
        admin_uname = self.driver.find_element(By.XPATH, "/html/body/div/div/div/form/div[1]/input")
        admin_pwd = self.driver.find_element(By.XPATH, "/html/body/div/div/div/form/div[2]/input")
        admin_submit = self.driver.find_element(By.XPATH, "/html/body/div/div/div/form/button")

        admin_uname.send_keys("admin@gmail.com")
        admin_pwd.send_keys("invalidpasswordbeenentered")
        admin_submit.click()

        try:
            # Explicitly wait for the error message element to be visible
            error_message = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, "/html/body/div/div/div/div"))
            ).text
        except NoSuchElementException:
            # If the error message element is not found, fail the test
            self.fail("Error message not found")

        self.assertEqual(error_message, "Wrong Email or Password")

        # Save a screenshot
        self.save_screenshot("login_failure")

if __name__ == "__main__":
    unittest.main()
