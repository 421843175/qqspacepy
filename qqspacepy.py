#coding:utf-8

import time
from selenium import webdriver
from lxml import etree
from importlib import reload
from selenium.webdriver.common.by import By
import sys
import imp
imp.reload(sys)
import datetime 

# TODO:账号密码
user = '' 
pw = ''
driver = webdriver.Chrome()
driver.maximize_window()
driver.get("http://i.qq.com")
driver.switch_to.frame("login_frame")
driver.find_element(By.ID,"switcher_plogin").click()
driver.find_element(By.ID,"u").send_keys(user)
driver.find_element(By.ID,"p").send_keys(pw)
driver.find_element(By.ID,"login_button").click()
driver.switch_to.default_content()

driver.get("http://user.qzone.qq.com/" + user + "/311")

next_num = 0  
while True:
        for i in range(1,6):
            height = 20000*i
            strWord = "window.scrollBy(0,"+str(height)+")"
            driver.execute_script(strWord)
            time.sleep(4)
        driver.switch_to.frame("app_canvas_frame")
        selector = etree.HTML(driver.page_source)
        divs = selector.xpath('//*[@id="msgList"]/li/div[3]')
        with open('qq_word.txt','a',encoding='utf-8') as f:
            for div in divs:
                qq_name = div.xpath('./div[2]/a/text()')
                qq_content = div.xpath('./div[2]/pre/text()')
                contentres=''
                for res in qq_content:
                    contentres=contentres+res
                qq_time = div.xpath('./div[4]/div[1]/span/a/text()')
                qq_name = qq_name[0] if len(qq_name)>0 else ''
                qq_time = qq_time[0] if len(qq_time)>0 else ''            
                qq_img = div.xpath("./div[3]/div[1]//a/@href")
                filtered_qq_img = filter(lambda x: "photo.store.qq.com" in x, qq_img)
                qq_img = list(filtered_qq_img)
                qq_img_str = ','.join(qq_img)
                contentres=contentres.replace("\n","");
                try:
                    qq_time = datetime.datetime.strptime(qq_time, '%Y年%m月%d日').strftime('%Y-%m-%d')
                except Exception:
                    pass
                # TODO:输出信息可以改
                insert_sql = "INSERT INTO record (content, createTime, srcPicArray) VALUES ('{}', '{}', '{}');".format(contentres, qq_time, qq_img_str)
                f.write(insert_sql)
                f.write("\n\n")
        if driver.page_source.find('pager_next_' + str(next_num)) == -1:
         break
        driver.find_element(By.ID,'pager_next_' + str(next_num)).click()
        next_num += 1
        driver.switch_to.parent_frame()