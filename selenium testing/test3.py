from selenium import webdriver
from selenium.webdriver.support.ui import Select

driver = webdriver.Chrome("C:\\Users\\mihir\\Downloads\\chromedriver_win32\\chromedriver.exe")

webapp = "http://desaimihir12.pythonanywhere.com/"

driver.get(webapp)

driver.find_element_by_id("exampleInputEmail1").send_keys("desaimihir12@gmail.com")

driver.find_element_by_id("exampleInputPassword1").send_keys("mihirdesai")

element = driver.find_element_by_xpath("/html/body/section/section/section/form/div[4]/a/button")

element.click()

driver.find_element_by_xpath("/html/body/div/form/div[1]/input").send_keys(-10)

list1 = Select(driver.find_element_by_id("from_c"))

list1.select_by_visible_text('United States Dollar')

list2 = Select(driver.find_element_by_id("to_c"))

list2.select_by_visible_text('Indian Rupee')

element2 = driver.find_element_by_xpath("/html/body/div/form/button")

element2.click()