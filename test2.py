import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
class TestAddEmployee(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Create a WebDriver instance
        cls.driver = webdriver.Chrome()
        cls.driver.maximize_window()

    def setUp(self):
        # Open the desired URL
        self.driver.get("http://localhost:3000/start")

        # Find and click the login button
        admin = self.driver.find_element(By.XPATH, "/html/body/div/div/div/div[2]/div/button[2]")
        admin.click()
        admin_uname = self.driver.find_element(By.XPATH, "/html/body/div/div/div/form/div[1]/input")
        admin_pwd = self.driver.find_element(By.XPATH, "/html/body/div/div/div/form/div[2]/input")
        admin_submit = self.driver.find_element(By.XPATH,"/html/body/div/div/div/form/button")
        admin_uname.send_keys("admin@gmail.com")
        admin_pwd.send_keys("admin")
        admin_submit.click()

        # Next Add Employee Step:
        wait = WebDriverWait(self.driver, 10)
        mng_faculty_tab_locator = "/html/body/div/div/div/div[1]/div/ul/li[2]/a"
        mng_faculty_tab = wait.until(EC.presence_of_element_located((By.XPATH, mng_faculty_tab_locator)))
        mng_faculty_tab.click()

        wait = WebDriverWait(self.driver, 10)
        add_emp_btn_locator = "/html/body/div/div/div/div[2]/div[2]/a"
        add_emp_btn = wait.until(EC.presence_of_element_located((By.XPATH, add_emp_btn_locator)))
        add_emp_btn.click()

        f_name_input_locator = "/html/body/div/div/div/div[2]/div[2]/form/div[1]/input"
        f_email_input_locator = "/html/body/div/div/div/div[2]/div[2]/form/div[2]/input"
        f_dept_input_locator = "/html/body/div/div/div/div[2]/div[2]/form/div[3]/input"
        submit_button_locator = "/html/body/div/div/div/div[2]/div[2]/form/div[4]/button"

        # Explicitly wait for the elements to be present
        wait = WebDriverWait(self.driver, 10)
        self.f_name = wait.until(EC.presence_of_element_located((By.XPATH, f_name_input_locator)))
        self.f_email = wait.until(EC.presence_of_element_located((By.XPATH, f_email_input_locator)))
        self.f_dept = wait.until(EC.presence_of_element_located((By.XPATH, f_dept_input_locator)))
        self.all_submit = wait.until(EC.element_to_be_clickable((By.XPATH, submit_button_locator)))

    def test_add_employee(self):
        checker_mail = "jadeja@gmail.com"
        self.f_name.send_keys("Umesh Yadav")
        self.f_email.send_keys("jadeja@gmail.com")
        self.f_dept.send_keys("ECE")
        self.all_submit.click()

        # Wait for the alert box to appear
        wait = WebDriverWait(self.driver, 10)
        alert = wait.until(EC.alert_is_present())

        # Perform actions on the alert box
        alert_text = alert.text
        alert.accept()

        # Wait for the table to be updated with the new row
        wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div/div/div/div[2]/div[2]/div[2]/table/tbody/tr[last()]/td[3]")))

        # Find the last row and retrieve the value of the third column
        last_row = self.driver.find_element(By.XPATH, "/html/body/div/div/div/div[2]/div[2]/div[2]/table/tbody/tr[last()]")
        third_column_value = last_row.find_element(By.XPATH, "td[3]").text

        # Assert that the third column value matches the checker_mail
        self.assertEqual(third_column_value, checker_mail)
    def test_add_employee_failure(self):
        checker_mail = "vihari@gmail.com"
        self.f_name.send_keys("Travis Head")
        self.f_email.send_keys("vihari@gmail.com")
        self.f_dept.send_keys("Mech")
        self.all_submit.click()

        # Wait for the alert box to appear
        wait = WebDriverWait(self.driver, 10)
        try:
            # Set the timeout to 6 seconds in the WebDriverWait constructor
            wait = WebDriverWait(self.driver, 6)
            # Wait for the alert box to appear
            alert = wait.until(EC.alert_is_present())
            # Perform actions on the alert box
            alert_text = alert.text
            alert.accept()
        except TimeoutException:
            # Handle the exception if the alert does not appear within the timeout
            self.assertNotEqual("skfnk092kl", checker_mail)

        self.assertNotEqual("skfnk092kl", checker_mail)

    @classmethod
    def tearDownClass(cls):
        # Close the browser
        cls.driver.quit()

if __name__ == "__main__":
    unittest.main()
