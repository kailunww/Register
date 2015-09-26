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
import webbrowser
from PIL import Image
import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "helper")))
import uuClient
cap_path = os.path.join(os.path.dirname(__file__), 'capcha.png')

old_password = 'aaaa2222'
new_password = "aaaa3333"
prefix = "j1020909c701"

def alert_handle(driver):
    try:
        time.sleep(3)
        alert = driver.switch_to_alert()
        alert.accept()  
    except:
        pass

def activate_account(username):
    try:
        print 'Activate ', username
        #username = 'j1020909c3a9002'
        #password = 'aaaa2222'
        driver = webdriver.Firefox()
        driver.implicitly_wait(30)
        #driver.set_window_size(100, 100)
        #driver.set_window_position(-200, -200)
        driver.get("http://www.isn99.com/membersite/login.jsp")
        time.sleep(2)  
        driver.find_element_by_id("username").send_keys(username)
        driver.find_element_by_id("password").send_keys(old_password)
        e_capcha = driver.find_element_by_class_name('captcha')
        rect = e_capcha.rect
        driver.save_screenshot(cap_path)
        # Crop the capcha
        im = Image.open(cap_path) # uses PIL library to open image in memory
        left = rect['x']
        top = rect['y']
        right = rect['x'] + rect['width']
        bottom = rect['y'] + rect['height']
        im = im.crop((left, top, right, bottom)) # defines crop points
        im.save('capcha.png') # saves new cropped image
        #Enter the capcha
        cap = ""
    #    webbrowser.open('capcha.png')
    #    while 1:
    #        cap = str(raw_input("Enter capcha: ")).strip()
    #        if len(cap) == 4:
    #            break
        cap = uuClient.get_capcha(cap_path)
        if cap == "" or len(cap) != 4:
            print "Cannont get capcha"
            return False
        driver.find_element_by_id("code").send_keys(cap)   
        driver.find_element_by_id("login").click()
        while "membersite" not in driver.current_url:
            time.sleep(1)  
        time.sleep(2)  
        driver.find_element_by_class_name("tnc-agree").click()   
        while 'membersite' not in driver.current_url:
            time.sleep(0.5) 
        time.sleep(2)  
        driver.find_element_by_name('oldPassword').send_keys(old_password)
        driver.find_element_by_name('newPassword').send_keys(new_password)
        driver.find_element_by_name('confirmPassword').send_keys(new_password)
        driver.find_element_by_class_name("changePassword").click()
        alert_handle(driver) 
        while 'membersite' not in driver.current_url:
            time.sleep(0.5) 
        time.sleep(2)  
        driver.find_element_by_class_name("updatePreference").click()
        alert_handle(driver)
        while 'membersite' not in driver.current_url:
            time.sleep(0.5)
        alert_handle(driver)
        nickname = username[0] + username[-9:]
        driver.find_element_by_id('loginName').send_keys(nickname)
        driver.find_element_by_class_name("confirmLogin").click()
        alert_handle(driver)
        time.sleep(1)
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
    #pwd = raw_input("Enter password: ").strip()
    activate_accounts(prefix, id_from, id_to)      
    raw_input("Press any key to quit.")
