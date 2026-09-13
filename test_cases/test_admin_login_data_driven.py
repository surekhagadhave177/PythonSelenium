import time

from selenium import webdriver
from selenium.webdriver.common.by import By

from base_pages.Login_Admin_page import Login_Admin_Page
from utilities import excel_utils
from utilities.custom_logger import Log_Maker
from utilities.read_properties import Read_Config


class Test02_Admin_Login_Data_Driven:
    admin_page_url = Read_Config.get_admin_page_url()
    logger=Log_Maker.log_gen()
    path=".//test_data//admin_lodi_data.xlsx"
    def test_valid_admin_login_data_driven(self,setup):
        self.logger.info("********test_valid_admin_login********")
        self.driver = setup
        self.driver.implicitly_wait(10)
        self.driver.get(self.admin_page_url)
        self.admin_lp = Login_Admin_Page(self.driver)

        self.rows = excel_utils.get_row_count(self.path, "Sheet1")
        print("num of rows", self.rows)
        for r in range(2, self.rows + 1):
            self.username = excel_utils.read_data(self.path, "Sheet1", r, 1)
            self.password = excel_utils.read_data(self.path, "Sheet1", r, 2)
            self.exp_login = excel_utils.read_data(self.path, "Sheet1", r, 3)
            self.admin_lp.enter_username(self.username)
            self.admin_lp.enter_password(self.password)
            self.admin_lp.click_login()
            time.sleep(5)


