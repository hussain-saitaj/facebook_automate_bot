from selenium import webdriver
from selenium.webdriver.common import keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import os
import time
from autoit import win
import autoit
import pandas as pd

driver = webdriver.Chrome()
driver.get("http://www.facebook.com")
wait = WebDriverWait(driver, 10)
login_id=driver.find_element_by_id("email")
login_pass=driver.find_element_by_id("pass")
login_btn=driver.find_element_by_name("login")
login_id.clear()
login_pass.clear()
login_id.send_keys("Your Login id")
login_pass.send_keys("Your Password")
login_btn.click()
wait.until(EC.url_changes('https://m.facebook.com/'))
driver.get('https://m.facebook.com/')
time.sleep(2)
file_read=pd.read_csv(r"C:\\Users\TAJ\projects\fb_automate\ProgrammingHumour\images\images.csv")
for i in range(len(file_read)):
    post=file_read['Title'][i]
    post_url=file_read['Url'][i]
    _, ext = os.path.splitext(post_url)
    #print(post,ext)
    post=post.replace('b','')
    post=post.replace("'","")
    ext=ext.replace("'","")
    #print(post,ext)
    path="C:\\Users\TAJ\projects\\"+"fb_automate\ProgrammingHumour\images"+"\\"+post+ext
    #print(path)
    whats_on_your_mind = driver.find_elements_by_class_name('_5xu4')[1].click()
    wait.until(EC.presence_of_element_located((By.ID, 'uniqid_1')))
    post_text_area = driver.find_element_by_xpath('//*[@id="uniqid_1"]')
    post_image=driver.find_element_by_xpath('//*[@id="structured_composer_form"]/div[6]/div/button[1]/div/div[2]').click()
    time.sleep(2)
    win.win_activate('Open')
    autoit.control_send("Open","Edit1",path) 
    autoit.control_send("Open","Edit1","{ENTER}")
    post_text_area.send_keys(post)
    post_btn = driver.find_element_by_xpath('/html/body/div[2]/div[1]/div/div[2]/div/div/div[5]/div[3]/div/div/button')
    post_btn.click()
    wait.until(EC.visibility_of_element_located((By.XPATH, "//*[contains(text(), 'Your post is now published.')]")))
    print('Post published successfully!')
driver.close()