from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import unittest

class NewVisitorTest(unittest.TestCase):

  def setUp(self):
    self.browser = webdriver.Firefox()

  def tearDown(self):
    self.browser.quit()

  def check_for_row_in_list_table(self, row_text):
    table = self.browser.find_element_by_id('id_list_table')
    rows = table.find_elements_by_tag_name('tr')
    self.assertIn(row_text, [row.text for row in rows])

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
    self.check_for_row_in_list_table('1: choke the chicken')

    # Not satisfied, he enters 'wrestle the snake'
    inputbox = self.browser.find_element_by_id('id_new_item')
    inputbox.send_keys('wrestle the snake')
    inputbox.send_keys(Keys.ENTER)
    time.sleep(1)

    # Lo and behold, the page now lists both items!
    self.check_for_row_in_list_table('1: choke the chicken')
    self.check_for_row_in_list_table('2: wrestle the snake')

    # Existential questions arise: will this list last?
    # Pondering this Henk notices the url; it's unique
    # Magically some text appeared, informing Henk the url is the key to persistance
    self.fail('Finish the test!')

    # Skeptically he visits this url in pron mode - aha! All is well

    # Satisfied, he goes back to sleep

if __name__ == '__main__':  
    # unittest.main(warnings='ignore') 
    unittest.main() 
