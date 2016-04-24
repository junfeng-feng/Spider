# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re
import time

class DianpingOpenMap(unittest.TestCase):
    def setUp(self):
        #self.driver = webdriver.Firefox()
        self.driver =webdriver.PhantomJS(executable_path="/Users/fengjunfeng/Documents/phantomjs-2.1.1-macosx/bin/phantomjs",
			service_log_path='/Users/fengjunfeng/Documents/phantomjs-2.1.1-macosx/log/ghostdriver.log')
        self.driver.implicitly_wait(30)
        self.base_url = "http://www.dianping.com"
        self.verificationErrors = []
        self.accept_next_alert = True
    
    def test_dianping_open_map(self):
        driver = self.driver
        driver.get(self.base_url + "/shop/11162894")
        driver.find_element_by_css_selector("#J_map-show > i.icon").click()
	print driver.page_source
#	time.sleep(15)
	
    
    def is_element_present(self, how, what):
        try: self.driver.find_element(by=how, value=what)
        except NoSuchElementException as e: return False
        return True
    
    def is_alert_present(self):
        try: self.driver.switch_to_alert()
        except NoAlertPresentException as e: return False
        return True
    
    def close_alert_and_get_its_text(self):
        try:
            alert = self.driver.switch_to_alert()
            alert_text = alert.text
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        finally: self.accept_next_alert = True
    
    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    unittest.main()
