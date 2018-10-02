# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary

ISOTIMEFORMAT = '%Y-%m-%d %X'  # Time setup


driver = webdriver.Firefox(executable_path='/Applications/Firefox.app/Contents/MacOS'
                           )

driver.get('http://www.asos.com/?hrd=1')

output = driver.find_elements_by_xpath("//a[@class='standard']")

for ele in output:
    print(ele.get_attribute('href'))
