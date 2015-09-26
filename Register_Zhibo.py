# -*- coding: utf-8 -*-
"""
Created on Tue Aug 18 22:12:33 2015

@author: User
"""

from selenium import webdriver
from selenium.webdriver.support.ui import Select
import time
from PIL import Image
import os, sys
import winsound
Freq = 1000 # Set Frequency To 2500 Hertz
Dur = 500 # Set Duration To 1000 ms == 1 second
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "helper")))
import uuClient

agent_username = 'j1020909c701'
agent_password = 'qqqq9998'
verification_code = '959595'
default_password = 'aaaa2222'
max_bet = '200,000'
credit = '5,000'
cap_path = os.path.join(os.path.dirname(__file__), 'capcha.png')

def register_account(id1,id2,id3):
    try:
        print 'Register %s%s%s starts' % (id1,id2,id3)
        driver.get(url_new)
        time.sleep(1)
        e1 = driver.find_element_by_id('agentUserName0')
        e2 = driver.find_element_by_id('agentUserName1')
        e3 = driver.find_element_by_id('agentUserName2')
        time.sleep(1)
        e1.send_keys(id1)
        time.sleep(1)
        e2.send_keys(id2)
        time.sleep(1)
        e3.send_keys(id3)
        driver.find_element_by_id('password').send_keys(default_password)
        driver.find_element_by_id('creditLimit').clear()
        driver.find_element_by_id('creditLimit').send_keys(credit)
        sid1 = Select(driver.find_element_by_id('agentUserName0')).first_selected_option.get_attribute("value")
        sid2 = Select(driver.find_element_by_id('agentUserName1')).first_selected_option.get_attribute("value")
        sid3 = Select(driver.find_element_by_id('agentUserName2')).first_selected_option.get_attribute("value")
        print "Selected %s%s%s" % (sid1,sid2,sid3)
        if "%s%s%s" % (sid1,sid2,sid3) != '%s%s%s' % (id1,id2,id3):
            winsound.Beep(Freq,Dur)
            raw_input("Press any key to continue.")
        e_button = None
        for e in driver.find_elements_by_name("submit"):
            if e.text != "":
                e_button = e
        e_button.click()
        #raw_input("Press any key to continue.")
        time.sleep(3)
        try:
            alert = driver.switch_to_alert()
            alert.accept()
        except:
            pass
        #driver.close()
        print 'Register %s%s%s ends' % (id1,id2,id3)
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
               #driver.switch_to_default_content()
               #time.sleep(30)
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
    driver.get("http://isn999.com/managersite/")
    time.sleep(2)
    driver.find_element_by_id("loginUsername").send_keys(agent_username)
    driver.find_element_by_id("loginPassword").send_keys(agent_password)
    e_capcha = driver.find_element_by_id('captchaImage')
    rect = e_capcha.rect
    driver.save_screenshot(cap_path)
    # Crop the capcha
    im = Image.open(cap_path) # uses PIL library to open image in memory
    left = rect['x']
    top = rect['y']
    right = rect['x'] + rect['width']
    bottom = rect['y'] + rect['height']
    im = im.crop((left, top, right, bottom)) # defines crop points
    im.save(cap_path) # saves new cropped image
    #Enter the capcha
    cap = ""
    cap = uuClient.get_capcha(cap_path)
    if cap == "":
        print "Cannont get capcha"
    driver.find_element_by_id("captcha").send_keys(cap)    
    driver.find_element_by_name("loginSubmit").click()
    while "balance" not in driver.current_url:
        time.sleep(0.5)
    url_new = ""
    for e in driver.find_elements_by_xpath("//a"):
        if "agentCreation" in e.get_attribute('href'):
            url_new = e.get_attribute('href')
            break
    if url_new != "":
        register_accounts(id_from, id_to)      
    raw_input("Press any key to quit.")