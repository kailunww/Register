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
import time

old_password = 'aaaa2222'
new_password = "aaaa3333"
prefix = "ehsc701"

def alert_handle(driver, action):
    try:
        time.sleep(3)
        alert = driver.switch_to_alert()
        if action == 0:
            alert.accept()  
        if action == 1:
            alert.dismiss()
    except:
        pass
    
def activate_account(username):
    try:
        print 'Activate ', username
        driver = webdriver.Firefox()
        driver.implicitly_wait(30)
        driver.get("https://www.sbobet.com/en/betting.aspx")
        time.sleep(1)
        driver.find_element_by_id("username").send_keys(username)
        driver.find_element_by_id("password").send_keys(old_password)
        driver.find_element_by_class_name("sign-in").click()
        while 'force-change-password' not in driver.current_url:
            time.sleep(0.5)
        driver.find_element_by_id('txtOldPwd').send_keys(old_password)
        driver.find_element_by_id('txtNewPwd1').send_keys(new_password)
        driver.find_element_by_id('txtNewPwd2').send_keys(new_password)
        driver.find_element_by_class_name("submit-btn").click()
        alert_handle(driver, 0)
        while 'Terms' not in driver.title:
            time.sleep(0.5)
        driver.find_element_by_xpath("//input[@value='I Agree']").click()
        alert_handle(driver, 1)
        driver.close()
        return True 
    except (WindowsError,selenium.common.exceptions.WebDriverException) as e:
        print e
        return False     
            
def activate_accounts(prefix, id_from, id_to):
    for tid in range(id_from, id_to+1):
        ids = str(tid).zfill(3)
        username = "%s%s" % (prefix, ids)
        while 1:
           if activate_account(username):
               break
        
if __name__ == "__main__":
    id_from = str(raw_input("Enter start id: ")).strip()
    id_from = int(id_from)
    id_to = str(raw_input("Enter end id: ")).strip()
    id_to = int(id_to)
    #pwd = raw_input("Enter password: ").strip()
    activate_accounts(prefix, id_from, id_to)      
    raw_input("Press any key to quit.")
