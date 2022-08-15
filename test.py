from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import requests

# initialize driver with browser
driver = webdriver.Chrome()
# test deployment url
url = "http://localhost:5000/"
driver.get(url)
response = requests.get(url)
try:
    assert response.status_code == 200
except:
    print(AssertionError)
finally:
    # finish the testing
    driver.quit()

