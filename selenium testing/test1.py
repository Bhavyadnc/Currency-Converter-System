from selenium import webdriver

driver = webdriver.Chrome("C:\\Users\\mihir\\Downloads\\chromedriver_win32\\chromedriver.exe")

webapp = "http://desaimihir12.pythonanywhere.com/"

driver.get(webapp)

driver.find_element_by_id("exampleInputEmail1").send_keys("desaimihir12@gmail.com")

driver.find_element_by_id("exampleInputPassword1").send_keys("Password1234*")

element = driver.find_element_by_xpath("/html/body/section/section/section/form/div[4]/a/button")

element.click()