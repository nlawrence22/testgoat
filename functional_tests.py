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

class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox(capabilities=caps)
        self.browser.implicitly_wait(3)
    
    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_later(self):

        # Sandy wants a better way to keep track of to-do items, and heard
        # about a new app she could try, so she finds its homepage.
        try:
            self.browser.get('http://localhost:8000')
        # Instead of your assert failing, you get a webdriver exception if 
        # there's nothing listening on port 8000. This could mask other 
        # failures.
        except WebDriverException as e:
            print("WebDriverException encountered: {}".format(e))
        
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

        # When she hits enter, the page updates, and now the page lists
        # "1: Buy groceries" as an item in a to-do list
        inputbox.send_keys(Keys.ENTER)

        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertTrue(
            any(row.text == '1: Buy groceries' for row in rows)
        )

        # There is still a text box inviting her to add another item. She
        # enters "Cook Dinner"
        self.fail('Finish the test!')

        # The page updates again, and now shows both items on her list

        # Sandy has to run to the store, but won't have her computer with her.
        # Then she sees that the site has generated a unique URL for her -- 
        # there is some explanatory text to that effect. 

        # She visits that URL - her to-do list is still there.

        # Satisfied, she turns off her computer
        browser.quit()
    
if __name__ == '__main__':
    unittest.main(warnings='ignore')    