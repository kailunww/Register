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

agent_username = 'hh8c701'
agent_password = 'qqqq9999'
default_password = 'aaaa2222'
max_bet = 200000
credit = 5000
cap_path = os.path.join(os.path.dirname(__file__), 'capcha.png')

def register_account(id1,id2,id3):
    try:
        print 'Register %s%s%s starts' % (id1,id2,id3)
        driver.get("https://aaa.pinnaclesports.com/Members/NewMember.aspx")
        while driver.title != "Pinnacle Sports":
            time.sleep(0.5)
        for i in range(10):
            Select(driver.find_element_by_id('ctl00_PCPH_AL3DDL')).select_by_index(i)
            time.sleep(1)
            driver.find_element_by_id('ctl00_PCPH_PTB').send_keys(Keys.NULL)
            time.sleep(1)
            if id1 in [opt.text for opt in Select(driver.find_element_by_id('ctl00_PCPH_AL1DDL')).options]:
                break
        driver.find_element_by_id('ctl00_PCPH_AL1DDL').send_keys(id1)
        for i in range(10):
            Select(driver.find_element_by_id('ctl00_PCPH_AL3DDL')).select_by_index(i)
            time.sleep(1)
            driver.find_element_by_id('ctl00_PCPH_PTB').send_keys(Keys.NULL)
            time.sleep(1)
            if id2 in [opt.text for opt in Select(driver.find_element_by_id('ctl00_PCPH_AL2DDL')).options]:
                break
        driver.find_element_by_id('ctl00_PCPH_AL2DDL').send_keys(id2)
        for i in range(3):
            driver.find_element_by_id('ctl00_PCPH_AL3DDL').click()
            time.sleep(1)
            driver.find_element_by_id('ctl00_PCPH_PTB').send_keys(Keys.NULL)
            time.sleep(1)
            if id3 in [opt.text for opt in Select(driver.find_element_by_id('ctl00_PCPH_AL3DDL')).options]:
                break
        driver.find_element_by_id('ctl00_PCPH_AL3DDL').send_keys(id3)
        driver.find_element_by_id('ctl00_PCPH_PTB').send_keys(default_password)
        driver.find_element_by_id('ctl00_PCPH_MCTB').send_keys(credit)
        driver.find_element_by_id('ctl00_PCPH_OTDDL').send_keys('Hong Kong Odds')
        driver.find_element_by_id('ctl00_PCPH_CDDL').send_keys('China')
        driver.find_element_by_id('ctl00_PCPH_CustomerWagerMaxSelectionCtrl_DDWagerMaximumSelection').send_keys('Regular Maximums')
        driver.find_element_by_id('ctl00_PCPH_CaptchaControl_InputTB').send_keys(Keys.NULL)
        sid1 = Select(driver.find_element_by_id('ctl00_PCPH_AL1DDL')).first_selected_option.get_attribute("value")
        sid2 = Select(driver.find_element_by_id('ctl00_PCPH_AL2DDL')).first_selected_option.get_attribute("value")
        sid3 = Select(driver.find_element_by_id('ctl00_PCPH_AL3DDL')).first_selected_option.get_attribute("value")
        print "Selected %s%s%s" % (sid1,sid2,sid3)
        e_capcha = driver.find_element_by_id('ctl00_PCPH_CaptchaControl_CaptchaImg')
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
        # Enter the capcha
        cap = ""
        cap = uuClient.get_capcha(cap_path)
        if cap == "":
            print "Cannont get capcha"
            return False
        driver.find_element_by_id('ctl00_PCPH_CaptchaControl_InputTB').send_keys(cap)
        if "%s%s%s" % (sid1,sid2,sid3) != '%s%s%s' % (id1,id2,id3):
            winsound.Beep(Freq,Dur)
            raw_input("Press any key to continue.")
        driver.find_element_by_id("ctl00_PCPH_CRB").click()
        time.sleep(5)
        while 1:
            if "TaskMonitor" in driver.current_url:
                print "Success"
                print 'Register %s%s%s ends' % (id1,id2,id3)
                return True
            elif "NewMember" in driver.current_url:
                print "Fail"
                print 'Register %s%s%s ends' % (id1,id2,id3)
                return False
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
    driver.implicitly_wait(30)
    driver.get("https://aaa.pinnaclesports.com/")
    while driver.title != "Login":
        time.sleep(0.5)
    driver.find_element_by_id("UserName").send_keys(agent_username)
    driver.find_element_by_id("Password").send_keys(agent_password)
    driver.find_element_by_id("LB").click()
    while driver.title != "Pinnacle Sports":
        if driver.title == "Already Logged In":
            driver.find_element_by_id("COB").click()
        else:
            time.sleep(0.5)
    register_accounts(id_from, id_to)      
    raw_input("Press any key to quit.")