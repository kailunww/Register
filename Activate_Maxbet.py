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
import win32process, win32api, win32con
import os

old_password = 'Aaaa2222'
new_password = "aaa333**"
prefix = "PYRC701"

def kill_chrome():
    processes = win32process.EnumProcesses()    # get PID list
    for pid in processes:
        try:
            handle = win32api.OpenProcess(win32con.PROCESS_ALL_ACCESS, False, pid)
            exe = win32process.GetModuleFileNameEx(handle, 0)
            if 'chrome' in exe.lower():
                os.kill(pid, 4)
        except:
            pass
                
def activate_account(username):
    try:
        print 'Activate ', username
        kill_chrome()
        chrome_options = webdriver.ChromeOptions()
        #chrome_options.add_argument("--incognito")
        chrome_options.add_argument("--user-data-dir=")
        
        driver = webdriver.Chrome(chrome_options=chrome_options)
        driver.maximize_window()
        driver.get('http://www.maxbet.com/Default.aspx')
        driver.find_element_by_id('txtID').send_keys(username)
        driver.find_element_by_id('txtPW').send_keys(old_password)
        driver.find_element_by_class_name('button').click()
        while 'rulesalert' not in driver.current_url:
            time.sleep(0.5)
        time.sleep(3)
        driver.find_element_by_class_name('mark').click()
        time.sleep(3)
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
