from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import unittest

class NewVisitorTest(unittest.TestCase):

  def setUp(self):
    self.browser = webdriver.Firefox()

  def tearDown(self):
    self.browser.quit()

  def test_can_start_a_list_and_get_it_later(self):
    # Henk decides to visit this awesome thing he heard about
    self.browser.get('http://localhost:8000')

    # He sees the page title and header mention to-do lists
    self.assertIn('To-Do', self.browser.title)
    header_text = self.browser.find_element_by_tag_name('h1').text
    self.assertIn('To-Do', header_text)

    # Toroughly amazed, he immediately want to enter a to-do item
    inputbox = self.browser.find_element_by_id('id_new_item')
    self.assertEqual(
      inputbox.get_attribute('placeholder'),
      'Enter a to-do item'
    )

    # He types 'choke the chicken' into a text box
    inputbox.send_keys('choke the chicken')

    # When he hits enter, the page updates and now lists
    # 'choke the chicken' as an item in a to-do list
    inputbox.send_keys(Keys.ENTER)
    time.sleep(1)

    table = self.browser.find_element_by_id('id_list_table')
    rows = table.find_elements_by_tag_name('tr')
    self.assertTrue(
      any(row.text == '1: choke the chicken' for row in rows),
      "New to-do item did not appear in table"
    )

    # Not satisfied, he enters 'wrestle the snake'
    self.fail('Finish the test!')

    # Lo and behold, the page now lists both items!

    # Existential questions arise: will this list last?
    # Pondering this Henk notices the url; it's unique
    # Magically some text appeared, informing Henk the url is the key to persistance

    # Skeptically he visits this url in pron mode - aha! All is well

    # Satisfied, he goes back to sleep

if __name__ == '__main__':  
    # unittest.main(warnings='ignore') 
    unittest.main() 
