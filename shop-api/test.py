from selenium import webdriver
from selenium.webdriver import Chrome

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

chromeOptions = webdriver.ChromeOptions()
chromeOptions.add_argument("--no-sandbox")
chromeOptions.add_argument("--headless")


driver = Chrome(options=chromeOptions)
driver.get("http://www.python.org")
assert "Python" in driver.title

searchBox = driver.find_element(By.ID, "id-search-field")
searchBoxText = searchBox.get_attribute("placeholder")
print('original search text={0}'.format(searchBoxText))

testString = "pycon"
searchBox.clear()
searchBox.send_keys(testString)
print('our search text={0}'.format(testString))
searchBox.send_keys(Keys.RETURN)

searchResult = driver.find_element(By.CLASS_NAME, "list-recent-events")
searchItem = searchResult.find_elements(By.TAG_NAME, "li")
print("search result count={0}".format(len(searchItem)))

driver.close()
