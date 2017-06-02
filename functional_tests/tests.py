from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
import time

MAX_WAIT = 5

class NewVisitorTest(LiveServerTestCase):

  def setUp(self):
    self.browser = webdriver.Chrome()

  def tearDown(self):
    self.browser.quit()

  def wait_for_row_in_list_table(self, row_text):
    start_time = time.time()
    while True:
      try:
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])
        return
      except (AssertionError, WebDriverException) as e:
        if time.time() - start_time > MAX_WAIT:
          raise e
        time.sleep(0.1)

  def test_can_start_a_list_for_one_user(self):
    # Henk decides to visit this awesome thing he heard about
    self.browser.get(self.live_server_url)

    # He sees the page title and header mention to-do lists
    self.assertIn('To-Do', self.browser.title)
    header_text = self.browser.find_element_by_tag_name('h1').text
    self.assertIn('To-Do', header_text)

    # Toroughly amazed, he immediately wants to enter a to-do item
    self.browser.get(self.live_server_url)
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
    self.wait_for_row_in_list_table('1: choke the chicken')

    # Not satisfied, he enters 'wrestle the snake'
    inputbox = self.browser.find_element_by_id('id_new_item')
    inputbox.send_keys('wrestle the snake')
    inputbox.send_keys(Keys.ENTER)

    # Lo and behold, the page now lists both items!
    self.wait_for_row_in_list_table('1: choke the chicken')
    self.wait_for_row_in_list_table('2: wrestle the snake')

    # Satisfied, he goes back to sleep


  def test_multiple_users_can_start_lists_at_different_urls(self):
    # Henk decides to create a new todo list
    self.browser.get(self.live_server_url)
    inputbox = self.browser.find_element_by_id('id_new_item')
    inputbox.send_keys('choke the chicken')
    inputbox.send_keys(Keys.ENTER)
    self.wait_for_row_in_list_table('1: choke the chicken')
    
    # Existential questions arise: will this list last?
    # Pondering this Henk notices the url; it's unique
    # Magically some text appeared, informing Henk the url is the key to persistance
    henk_list_url = self.browser.current_url
    self.assertRegex(henk_list_url, '/lists/.+')

    # Shiver me timbers! A new user appears!

    ## To accurately simulate this, we restart the browser
    self.browser.quit()
    self.browser = webdriver.Chrome()

    # Sjaak visits /. There is no list to be found
    self.browser.get(self.live_server_url)
    page_text = self.browser.find_element_by_tag_name('body').text
    self.assertNotIn('choke the chicken', page_text)
    self.assertNotIn('make a fly', page_text)
 
    # Sjaak creates a list for himself - he is a bit less direct than Henk
    inputbox = self.browser.find_element_by_id('id_new_item')
    inputbox.send_keys('water the plants')
    inputbox.send_keys(Keys.ENTER)
    self.wait_for_row_in_list_table('1: water the plants')
 
    # The system is feeling generous and also gives Sjaak a unique url
    sjaak_list_url = self.browser.current_url
    self.assertRegex(sjaak_list_url, '/lists/.+')
    self.assertNotEqual(sjaak_list_url, henk_list_url)

    # There still is no trace of Henk's list
    page_text = self.browser.find_element_by_tag_name('body').text
    self.assertNotIn('choke the chicken', page_text)
    self.assertIn('water the plants', page_text)

    # Satisfied, he goes back to sleep

  def test_layout_and_styling(self):
    # Henk decides to visit the homepage again
    self.browser.get(self.live_server_url)
    self.browser.set_window_size(1024, 768)

    # He relishes in the awesomeness of a centered input box
    inputbox = self.browser.find_element_by_id('id_new_item')
    self.assertAlmostEqual(
      inputbox.location['x'] + inputbox.size['width'] / 2,
      512,
      delta=10
    )

    # He starts a new list and basks in the renewed 'centeredness' of the input box
    inputbox.send_keys('truth lies in the')
    inputbox.send_keys(Keys.ENTER)
    self.wait_for_row_in_list_table('1: truth lies in the')
    inputbox = self.browser.find_element_by_id('id_new_item')
    self.assertAlmostEqual(
      inputbox.location['x'] + inputbox.size['width'] / 2,
      512,
      delta=10
    )

