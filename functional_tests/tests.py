from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.keys import Keys
import unittest

# The default firefoxDriver no longer plays nice with FF 48+ so we need to use
# the marionette driver instead.  Details here:
# https://developer.mozilla.org/en-US/docs/Mozilla/QA/Marionette/WebDriver
caps = DesiredCapabilities.FIREFOX
caps["marionette"] = True
caps["binary"] = "/Applications/Firefox.app/Contents/MacOS/firefox-bin"

class NewVisitorTest(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox(capabilities=caps)
        self.browser.implicitly_wait(3)
    
    def tearDown(self):
        self.browser.quit()

    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])

    def test_can_start_a_list_and_retrieve_later(self):

        # Sandy wants a better way to keep track of to-do items, and heard
        # about a new app she could try, so she finds its homepage.
        self.browser.get(self.live_server_url)
 
        # She notices the homepage and header has To-Do in the title
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        # She is invited to enter a to-do item straight away
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
                inputbox.get_attribute('placeholder'),
                'Enter a to-do item'
        )

        # She types "Buy groceries" into a text box
        inputbox.send_keys('Buy groceries')

        # When she hits enter, she is taken to a new URL. The page now lists
        # "1: Buy groceries" as an item in a to-do list table.
        inputbox.send_keys(Keys.ENTER)
        sandy_list_url = self.browser.current_url
        self.assertRegex(sandy_list_url, '/lists/.+')

        import time
        time.sleep(1)
        self.check_for_row_in_list_table('1: Buy groceries')
        

        # There is still a text box inviting her to add another item. She
        # enters "Cook Dinner"
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Cook Dinner')
        inputbox.send_keys(Keys.ENTER)

        time.sleep(1)
        # The page updates again, and now shows both items on her list
        self.check_for_row_in_list_table('1: Buy groceries')
        self.check_for_row_in_list_table('2: Cook Dinner')

        # Now a new user, Nicholas, comes to the site.

        ## We use a new browser session to ensure isolation, i.e. that no
        ## cookies, cache, etc. are bleeding over from the previous portions
        ## of the test.
        self.browser.quit()
        self.browser = webdriver.Firefox(capabilities=caps)

        # Nicholas visits the homepage.  There is no sign of Sandy's list
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy groceries', page_text)
        self.assertNotIn('Cook Dinner', page_text)

        # Nicholas starts a new list by entering a new item.  He is more
        # exciting than Sandy...
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Go skydiving')
        inputbox.send_keys(Keys.ENTER)

        # Nicholas gets his own unique URL
        nicholas_list_url = self.browser.current_url
        self.assertRegex(nicholas_list_url, 'lists/.+')
        self.assertNotEqual(nicholas_list_url, sandy_list_url)

        #Again, there is no trace of Sandy's list
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy groceries', page_text)
        self.assertIn('Go skydiving')

        # Satisfied, she turns off her computer
        browser.quit()
    
if __name__ == '__main__':
    unittest.main(warnings='ignore')    