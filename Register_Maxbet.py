# -*- coding: utf-8 -*-
"""
Created on Tue Aug 18 22:12:33 2015

@author: User
"""

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time, os, sys
from PIL import Image
from selenium.webdriver.support.ui import Select
import winsound
Freq = 1000 # Set Frequency To 2500 Hertz
Dur = 500 # Set Duration To 1000 ms == 1 second
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "helper")))
import uuClient

agent_username = 'pyrc701'
agent_password = 'qqq..9999'
verification_code = '959595'
default_password = 'Aaaa2222'
max_bet = 200000
credit = 5000
cap_path = os.path.join(os.path.dirname(__file__), 'capcha.png')

def register_account(id1,id2,id3):
    try:
        print 'Register %s%s%s starts' % (id1,id2,id3)
        driver.switch_to_default_content()
        driver.switch_to_frame(driver.find_element_by_id('menu'))
        time.sleep(3)
        for e in driver.find_elements_by_tag_name('a'):
            if "New Member" in e.text:
                newmember = e
                break
        newmember.click()
        time.sleep(3)
        driver.switch_to_default_content()
        driver.switch_to_frame(driver.find_element_by_id('main'))
        driver.switch_to_frame(driver.find_element_by_id('frmAddNewMember'))
        time.sleep(0.5)
        driver.find_element_by_id("txtUserName").clear()
        time.sleep(0.5)
        driver.find_element_by_id("txtUserName").send_keys('PYRC701000')
        time.sleep(0.5)
        driver.find_element_by_id("sbuttonReView").click()
        time.sleep(3)
        driver.find_element_by_id("sbuttonNext").click()
        time.sleep(3)
        driver.find_element_by_id("txtCredit").send_keys(credit)
        time.sleep(0.5)
        driver.find_element_by_id("txtPwd").send_keys(default_password)
        time.sleep(0.5)
        driver.find_element_by_id("Number1").send_keys(id1)
        time.sleep(0.5)
        driver.find_element_by_id("Number2").send_keys(id2)
        time.sleep(0.5)
        driver.find_element_by_id("Number3").send_keys(id3)
        time.sleep(0.5)
        driver.find_element_by_id("sbuttonNext").click()
        time.sleep(10)
        while 1:
			e_capcha = None
            try:
                driver.switch_to_default_content()
                main = driver.find_element_by_id('main')
                rect1 = main.rect
                driver.switch_to_frame(main)
                addnew = driver.find_element_by_id('frmAddNewMember')
                rect2 = addnew.rect
                driver.switch_to_frame(addnew)
                frCaptcha = driver.find_element_by_id('frCaptcha')
                rect3 = frCaptcha.rect
                driver.switch_to_frame(driver.find_element_by_id('frCaptcha'))
                e_capcha = driver.find_element_by_id('CaptchaImage')
            except:
                break
            if e_capcha is None:
                break
            rect = e_capcha.rect
            driver.save_screenshot(cap_path)
            # Crop the capcha
            im = Image.open(cap_path) # uses PIL library to open image in memory
            x = rect['x'] + rect1['x'] + rect2['x'] + rect3['x']
            y = rect['y'] + rect1['y'] + rect2['y'] + rect3['y']
            left = x
            top = y
            right = x + rect['width']
            bottom = y + rect['height']
            im = im.crop((left, top, right, bottom)) # defines crop points
            im.save(cap_path) # saves new cropped image
            # Enter the capcha
            cap = ""
            for i in range(3):
                cap = uuClient.get_capcha(cap_path)
                if cap != "":
                    break
            else:
                return False
            driver.find_element_by_id("recaptcha_response_field").send_keys(cap)  
            driver.find_element_by_id("SubmitCaptcha").click()
            time.sleep(2)
            driver.switch_to_default_content()
            driver.switch_to_frame(driver.find_element_by_id('main'))
            driver.switch_to_frame(driver.find_element_by_id('frmAddNewMember'))
            driver.find_element_by_id("sbuttonNext").click()
            time.sleep(10)
        time.sleep(30)
        return True
    except Exception as e:
        print e
        return False
            
def register_accounts(id_from, id_to):
    for tid in range(id_from, id_to+1):
        ids = str(tid).zfill(3)
        id1 = ids[0]
        id2 = ids[1]
        id3 = ids[2]
        #print (id1, id2, id3)
        while 1:
           if register_account(id1, id2, id3):
               break
        
if __name__ == "__main__":
    id_from = str(raw_input("Enter start id: ")).strip()
    id_from = int(id_from)
    id_to = str(raw_input("Enter end id: ")).strip()
    id_to = int(id_to)
    while 1:
        try:
            driver = webdriver.Firefox()
        except WindowsError as e:
            print e
        else:
            break
    driver.implicitly_wait(10)
    driver.maximize_window()
    driver.get("http://www.ultra88.com")
    while driver.title != "Login":
        time.sleep(0.5)
    driver.find_element_by_id("txtUserName").send_keys(agent_username)
    time.sleep(1)
    driver.find_element_by_id("txtPassWord").send_keys(Keys.NULL)
    time.sleep(1)
    driver.find_element_by_id("txtPassWord").send_keys(agent_password)
    time.sleep(1)
    driver.find_element_by_id("btnLogin").click()
    while 'ultra88' not in driver.title:
            time.sleep(0.5)
    driver.switch_to_frame(driver.find_element_by_id('main'))
    time.sleep(0.5)
    driver.find_element_by_id("txtSecCode").send_keys(Keys.NULL)
    time.sleep(0.5)
    driver.find_element_by_id("txtSecCode").send_keys(verification_code)
    time.sleep(0.5)
    driver.find_element_by_xpath("//input[@value='Submit']").click()
    driver.switch_to_default_content()
    while 'Index.aspx' not in driver.current_url:
        time.sleep(0.5)
    register_accounts(id_from, id_to) 
      
    raw_input("Press any key to quit.")
    
    

