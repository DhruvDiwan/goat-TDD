from selenium import webdriver

browser = webdriver.Firefox()
browser.get('http://localhost:8000')

assert 'To-do' in browser.title , "browser title was " + browser.title
browser.quit()