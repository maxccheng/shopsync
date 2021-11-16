from selenium import webdriver
from selenium.webdriver import Chrome

from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC

#from fake_useragent import UserAgent




#### browser session options
chromeOptions = webdriver.ChromeOptions()
chromeOptions.add_argument("--no-sandbox")
chromeOptions.add_argument("--headless")
chromeOptions.add_argument("--disable-blink-features")
chromeOptions.add_argument("--disable-blink-features=AutomationControlled")
chromeOptions.add_argument("--window-size=1920,1080")
#uagent = UserAgent()
#userAgent = uagent.random
#print(userAgent)
#chromeOptions.add_argument(f'user_agent={userAgent}')
timeout = 2

driver = Chrome(options=chromeOptions)
driver.implicitly_wait(timeout)
driver.get("https://sellercenter.lazada.com.my")




#### sign in process
print("SIGN IN:")

str_user ="+60174799829"
str_password ="popo1234"

input_user = driver.find_element(By.XPATH, "//input[@id='account']")
input_user.clear()
input_user.send_keys(str_user)
print("Login user={0}".format(input_user.get_attribute('value')))

input_password = driver.find_element(By.XPATH, "//input[@id='password']")
input_password.clear()
input_password.send_keys(str_password)
print("Login password={0}".format(input_password.get_attribute('value')))

btn_login = driver.find_element(By.XPATH, "//span[text()='Login']/..")
sometext = btn_login.find_element(By.XPATH, "./span")
ActionChains(driver).move_to_element(btn_login).click().perform()

profile = driver.find_element(By.XPATH, "//div[contains(@class,'asc-profile-info')]/a")
print("Login success shop name={0}".format(profile.get_attribute('innerHTML')))




#### logout

driver.close()

