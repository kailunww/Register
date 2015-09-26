# -*- coding: utf-8 -*-
"""
Created on Tue Aug 18 22:12:33 2015

@author: User
"""

import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import time
import webbrowser
from PIL import Image
import contextlib
import os, sys
import winsound
Freq = 1000 # Set Frequency To 2500 Hertz
Dur = 500 # Set Duration To 1000 ms == 1 second
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "helper")))
import uuClient

agent_username = 'ehsc701sub00'
agent_password = 'qqq..9999'
verification_code = '959595'
default_password = 'aaaa2222'
max_bet = '200,000'
max_bet_per_match = '500,000'
credit = '5,000'
cap_path = os.path.join(os.path.dirname(__file__), 'capcha.png')

def register_account(id1,id2,id3):
    try:
        print 'Register %s%s%s starts' % (id1,id2,id3)
        driver.get(url_new)
        while 1:
            if "Security" in driver.title:
                udict = {
                    'first':1,
                    'second':2,
                    'third':3,
                    'fourth':4,
                    'fifth':5,
                    'sixth':6,
                }
                digit1 = udict[driver.find_elements_by_tag_name("strong")[0].text]
                digit2 = udict[driver.find_elements_by_tag_name("strong")[1].text]
                print digit1,digit2
                driver.find_element_by_id("digit1").send_keys(verification_code[digit1-1])
                driver.find_element_by_id("digit2").send_keys(verification_code[digit2-1])
                driver.find_element_by_xpath("//input[@type='submit']").click()
                break
            else:
                break
        time.sleep(2)
        for handle in driver.window_handles:
            driver.switch_to_window(handle)
        e1 = driver.find_element_by_id('account0')
        e2 = driver.find_element_by_id('account1')
        e3 = driver.find_element_by_id('account2')
        e1.send_keys(id1)
        e2.send_keys(id2)
        e3.send_keys(id3)
        driver.find_element_by_id('TextPassword').send_keys(default_password)
        driver.find_element_by_id('TextCredit').clear()
        driver.find_element_by_id('TextCredit').send_keys(credit)
        driver.find_element_by_id('TextMaxBet').clear()
        driver.find_element_by_id('TextMaxBet').send_keys(max_bet)
        driver.find_element_by_id('TextMaxPerMatch').clear()
        driver.find_element_by_id('TextMaxPerMatch').send_keys(max_bet_per_match)
        
        sid1 = Select(driver.find_element_by_id('account0')).first_selected_option.get_attribute("value")
        sid2 = Select(driver.find_element_by_id('account1')).first_selected_option.get_attribute("value")
        sid3 = Select(driver.find_element_by_id('account2')).first_selected_option.get_attribute("value")
        print "Selected %s%s%s" % (sid1,sid2,sid3)
        e_capcha = driver.find_element_by_id('imgText')
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
        webbrowser.open(cap_path)
        #winsound.Beep(Freq,Dur)
        while 1:
            cap = str(raw_input("Enter capcha: ")).strip()
            if len(cap) == 6:
                break
        driver.find_element_by_id('vcode').send_keys(cap)
        if "%s%s%s" % (sid1,sid2,sid3) != '%s%s%s' % (id1,id2,id3):
            winsound.Beep(Freq,Dur)
            raw_input("Press any key to continue.")
        driver.find_element_by_name("Button22").click()
        time.sleep(5)
        alert = driver.switch_to_alert()
        print alert.text
        if "success" in alert.text:
            alert.accept()
            #driver.close()
            print 'Register %s%s%s ends' % (id1,id2,id3)
            return True
        elif "busy" in alert.text:
            alert.accept()
            time.sleep(60)
            return False
        else:
            alert.accept()
            return False
    except selenium.common.exceptions.NoSuchElementException as e:
        print e
        return False
    except Exception as e:
        print e
        #winsound.Beep(Freq,Dur)
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
               driver.switch_to_default_content()
               break
        time.sleep(60)
          
        
if __name__ == "__main__":
    id_from = str(raw_input("Enter start id: ")).strip()
    id_from = int(id_from)
    id_to = str(raw_input("Enter end id: ")).strip()
    id_to = int(id_to)
    #default_password = raw_input("Enter password: ").strip()
#with contextlib.closing(webdriver.Firefox()) as driver:
    while 1:
        try:
            driver = webdriver.Firefox()
        except WindowsError as e:
            print e
        else:
            break
    driver.implicitly_wait(30)
    #driver.set_window_size(100, 100)
    #driver.set_window_position(-200, -200)
    driver.get("https://agent.sbobet.com ")
    while driver.title != "Sign In":
        time.sleep(0.5)
    driver.find_element_by_id("username").send_keys(agent_username)
    driver.find_element_by_id("password").send_keys(agent_password)
    e_capcha = driver.find_element_by_id('imgImgText')
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
    driver.find_element_by_id("vcode").send_keys(cap)    
    driver.find_element_by_id("btnSubmit").click()
    while 1:
        if 'processlogin' in driver.current_url or "Security" in driver.title:
            udict = {
                'first':1,
                'second':2,
                'third':3,
                'fourth':4,
                'fifth':5,
                'sixth':6,
            }
            digit1 = udict[driver.find_elements_by_tag_name("strong")[0].text]
            digit2 = udict[driver.find_elements_by_tag_name("strong")[1].text]
            print digit1,digit2
            driver.find_element_by_id("digit1").send_keys(verification_code[digit1-1])
            driver.find_element_by_id("digit2").send_keys(verification_code[digit2-1])
            driver.find_element_by_id("btnSubmit").click()
        elif 'home' in driver.current_url:
            break
        time.sleep(2)
    url = driver.current_url
    s1 = url.find('home.aspx')
    url_new = url[:s1] + 'membermgmt/member_new.aspx'
    register_accounts(id_from, id_to)      
    raw_input("Press any key to quit.")
