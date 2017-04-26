from selenium import webdriver

browser = webdriver.Firefox()

# Henk decides to visit this awesome thing he heard about
browser.get('http://localhost:8000')

# He sees the page title mention to-do lists
assert 'To-Do' in browser.title

# Toroughly amazed, he immediately want to enter a to-do item

# He types 'choke the chicken' into a text box

# When he hits enter, the page updates and now lists
# 'choke the chicken' as an item in a to-do list

# Not satisfied, he enters 'wrestle the snake'

# Lo and behold, the page now lists both items!

# Existential questions arise: will this list last?
# Pondering this Henk notices the url; it's unique
# Magically some text appeared, informing Henk the url is the key to persistance

# Skeptically he visits this url in pron mode - aha! All is well

# Satisfied, he goes back to sleep

browser.quit()