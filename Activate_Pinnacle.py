# -*- coding: utf-8 -*-
"""
Created on Wed Aug 19 00:46:30 2015

@author: User
"""
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 18 22:12:33 2015

@author: User
"""

import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import webbrowser
from PIL import Image
import contextlib
from selenium.webdriver.support.ui import Select

old_password = 'aaaa2222'
new_password = "aaa333**"
prefix = "hh8c701"

def activate_account(username):
    try:
        print 'Activate ', username
        driver = webdriver.Firefox()
        driver.implicitly_wait(30)
        driver.get("https://www.pinnaclesports.com/en/login")
        while 'Login' not in driver.title:
            time.sleep(0.5)
        driver.find_element_by_class_name("customerId").send_keys(username)
        driver.find_element_by_class_name("password").send_keys(old_password)
        driver.find_element_by_class_name("loginSubmit").click()
        while 'PasswordReset' not in driver.current_url:
            time.sleep(0.5)
        driver.find_element_by_id('CurrentPassword').send_keys(old_password)
        driver.find_element_by_id('NewPassword').send_keys(new_password)
        driver.find_element_by_id('ConfirmPassword').send_keys(new_password)
        driver.find_element_by_id("passwordResetButton").click()
        time.sleep(5)
        driver.close()
        return True
    except (WindowsError,selenium.common.exceptions.WebDriverException) as e:
        print e
        return False    
            
            
def activate_accounts(prefix, id_from, id_to):
    for tid in range(id_from, id_to+1):
        ids = str(tid).zfill(3)
        username = "%s%s" % (prefix, ids)
        #print (id1, id2, id3)
        while 1:
            
           if activate_account(username):
               break
        
if __name__ == "__main__":
    id_from = str(raw_input("Enter start id: ")).strip()
    id_from = int(id_from)
    id_to = str(raw_input("Enter end id: ")).strip()
    id_to = int(id_to)
    activate_accounts(prefix, id_from, id_to)      
    raw_input("Press any key to quit.")
