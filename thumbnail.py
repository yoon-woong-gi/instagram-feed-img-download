# noodle.zip 이라는 계정에 최신 피드 썸네일 9개 열기
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

from photo_down import information

def information() :
    global id, password, search_id, feed, times
    id=input('아이디를 입력해주세요 : ')
    password  = input('비밀번호를 입력해주세요 : ')
    search_id = input('검색 할 아이디를 입력해주세요 : ')

information()

driver = webdriver.Chrome('/Users/yoon/Desktop/instaPhoto/chromedriver')
driver.get('https://instagram.com')
time.sleep(2)

a = driver.find_elements_by_class_name('_2hvTZ')[0]
a.send_keys(id)

a = driver.find_elements_by_class_name('_2hvTZ')[1]
a.send_keys(password)
a.send_keys(Keys.ENTER)
 
time.sleep(4)

a = driver.find_elements_by_class_name('yWX7d')[0]
a.click()

time.sleep(2)

a = driver.find_elements_by_class_name('_a9--')[0]
a.click()

driver.get(f'https://www.instagram.com/{search_id}/')
time.sleep(5)

for i in range(10):
    url = driver.find_elements_by_css_selector('._aagv > img')[i].get_attribute('src')
    driver.execute_script(f'window.open("{url}");')
