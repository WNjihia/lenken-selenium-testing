import os
import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains


class TestSelenium(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome(
            "os.getenv('CHROME_WEBDRIVER')")
        self.base_url = "http://lenken.andela.com"

    def signin(self, email, pwd):
        driver = self.driver
        driver.get(self.base_url)
        driver.find_element_by_class_name("sign-in-button").click()
        driver.find_element_by_xpath(
            "//input[@id='identifierId']").send_keys(email)
        driver.find_element_by_id("identifierNext").click()
        driver.implicitly_wait(10)
        driver.find_element_by_xpath(
            "//input[@name='password']").send_keys(pwd)
        element = driver.find_element_by_id("passwordNext")
        driver.execute_script("arguments[0].click();", element)

    def create_request(self):
        driver = self.driver
        driver.find_element_by_xpath("//button[@id='request-button']").click()
        element = driver.find_element_by_id("mentor")
        driver.execute_script("arguments[0].click();", element)
        driver.find_element_by_xpath(
            "//app-skills-dropdown[@id='undefined']/ul/li/button").click()
        return self.complete_request_form()

    def complete_request_form(self):
        driver = self.driver
        element = driver.find_element_by_xpath(
            "//app-skills-dropdown[@id='undefined']/ul/li/div/a[1]")
        skill = element.text
        element.click()
        driver.find_element_by_xpath(
            "//textarea[@id='description']").send_keys("text")
        driver.find_element_by_xpath(
            "//div[@class='form-group'][3]/app-skills-dropdown/ul/li/button").click()
        driver.find_element_by_xpath(
            "//div[@class='form-group'][3]/app-skills-dropdown/ul/li/div/a[2]").click()
        #set days to Monday
        driver.find_element_by_xpath(
            "//span[@class='checkbox-wrapper'][2]/label").click()
        modal = driver.find_element_by_class_name('mentor-request-modal')
        driver.execute_script("arguments[0].scrollBy(0, 1000);", modal)
        #set time to 12:00 AM
        driver.find_element_by_css_selector(
            ".form-group:nth-child(7) > div:nth-child(1) > .mentor-dropdown > app-drop-down > ul > .dropdown > .request-option").click()
        driver.find_element_by_css_selector(
            ".form-group:nth-child(7) > div:nth-child(1) > .mentor-dropdown > app-drop-down > ul > .dropdown > div > a:nth-child(1)").click()
        #set timezone to EAT
        driver.find_element_by_xpath(
            "//span[@id='timezone']/app-drop-down/ul/li/button").click()
        driver.find_element_by_xpath(
            "//span[@id='timezone']/app-drop-down/ul/li/div/a[2]").click()
        #set session duration to 1hour
        driver.find_element_by_xpath("//span[@value='-']").click()
        driver.find_element_by_id("btn-request").click()
        return skill

    def close_request_modal(self):
        driver = self.driver
        driver.find_element_by_class_name("white-button").click()

    def delete_request(self):
        driver = self.driver
        driver.get("https://lenken.andela.com/request-pool")
        driver.find_element_by_xpath("//div[@id='request-pool']/a[1]").click()
        driver.find_element_by_xpath("//input[@class='button delete']").click()
        driver.find_element_by_xpath("//div[@class='cancel-reason-box']").click()
        driver.find_element_by_xpath("//div[@class='input-field']/div[@class='dropdown-content']/a[1]").click()
        driver.find_element_by_xpath("//div[@class='cancel-options']/div[1]").click()
        driver.find_element_by_xpath("//div[@class='cancel-options']/div[1]").click()

    def filter_request(self):
        # filter by location, duration, skillset
        driver = self.driver
        #select seeking mentor
        element = driver.find_element_by_css_selector(
            "app-pool-filters > div > form > .side-contents:nth-child(2) > .mentor")
        driver.execute_script("arguments[0].click();", element)
        element = driver.find_element_by_css_selector(
            "#location > .all-filters > div > .drop-toggle")
        driver.execute_script("arguments[0].click();", element)
        #set location to Nairobi
        element = driver.find_element_by_css_selector(
            "#location > .all-filters > div > .drop-show > label:nth-child(3)")
        driver.execute_script("arguments[0].click();", element)
        #set skill to Adobe Illustrator
        element = driver.find_element_by_css_selector(
            "#skill-set > .all-filters > div > .drop-toggle")
        driver.execute_script("arguments[0].click();", element)
        element = driver.find_element_by_css_selector(
            "#skill-set > .all-filters > div > .drop-show > label:nth-child(1)")
        driver.execute_script("arguments[0].click();", element)
        #set length to 1 month
        element = driver.find_element_by_css_selector(
            "#length-filter > .all-filters > div > .drop-toggle")
        driver.execute_script("arguments[0].click();", element)
        element = driver.find_element_by_css_selector(
            "#length-filter > .all-filters > div > .drop-show > label:nth-child(1)")
        driver.execute_script("arguments[0].click();", element)

    def test_request_create(self):
        driver = self.driver
        self.signin("os.getenv('EMAIL')", "os.getenv('PASSWORD')")
        self.create_request()
        success_msg = driver.find_element_by_class_name("message")
        assert "Your request was successfully created." in success_msg.text

    def test_request_filter(self):
        driver = self.driver
        self.signin("os.getenv('EMAIL')", "os.getenv('PASSWORD')")
        skill = self.create_request()
        self.close_request_modal()
        self.filter_request()
        element = driver.find_element_by_xpath(
            "//div[@class='pool-body']/a[1]/div[@id='primaryskill']")
        self.assertEqual(skill, element.text)
        element = driver.find_element_by_xpath("//div[@class='pool-body']/a[1]/div[@id='duration']")
        assert "1 Month" in element.text
        element = driver.find_element_by_xpath("//div[@class='pool-body']/a[1]/div[@id='request-location']")
        assert "Nairobi" in element.text

    def tearDown(self):
        self.driver.quit()


if __name__ == "__main__":
    unittest.main()
