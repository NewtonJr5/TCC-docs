from selenium import webdriver
from selenium.webdriver.chrome.options import Options

options = Options()

driver = webdriver.Chrome(options=options)

driver.get("https://www.reddit.com/r/python.json")

print(driver.page_source[:1000])

driver.quit()