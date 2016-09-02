from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common.exceptions import WebDriverException

# The default firefoxDriver no longer plays nice with FF 48+ so we need to use
# the marionette driver instead.  Details here:
# https://developer.mozilla.org/en-US/docs/Mozilla/QA/Marionette/WebDriver
caps = DesiredCapabilities.FIREFOX
caps["marionette"] = True
caps["binary"] = "/Applications/Firefox.app/Contents/MacOS/firefox-bin"

browser = webdriver.Firefox(capabilities=caps)
# Instead of your assert failing, you get a webdriver exception if there's
# nothing listening on port 8000.  Note, this could mask other failures.
try:
    browser.get('http://localhost:8000')
except WebDriverException as e:
    print("WebDriverException encountered: {}".format(e))

assert 'Django' in browser.title