from gettext import find
from lib2to3.pgen2 import driver
from re import I
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time

def information() :
    global id, password, search_id, feed, times
    id=input('아이디를 입력해주세요 : ')
    password  = input('비밀번호를 입력해주세요 : ')
    search_id = input('검색 할 아이디를 입력해주세요 : ')
    feed = int(input('몇 번째 피드부터 이미지를 다운로드할까요? : '))
    times = int(input('몇 개의 피드를 다운로드할까요? : '))

def login(ID,PASSWORD) :
    a = driver.find_elements(By.CLASS_NAME,'_2hvTZ')[0] #id input tag class
    a.send_keys(ID)

    a = driver.find_elements(By.CLASS_NAME,'_2hvTZ')[1] #password input tag class
    a.send_keys(PASSWORD)
    a.send_keys(Keys.ENTER)
    time.sleep(5)

    driver.find_elements(By.CLASS_NAME,'yWX7d')[0].click() #로그인정보저장
    time.sleep(2)

    driver.find_elements(By.CLASS_NAME,'_a9--')[0].click() #알림설정
    time.sleep(0.5)

def profile_info() :
    global p_img, p_post, p_follower, p_follow, p_name, p_bio
    p_img = driver.find_elements(By.CLASS_NAME,'_aa8j')[0].get_attribute('src')
    p_post = driver.find_elements(By.CLASS_NAME,'_ac2a')[0].text
    p_follower = driver.find_elements(By.CLASS_NAME,'_ac2a')[1].text
    p_follow = driver.find_elements(By.CLASS_NAME,'_ac2a')[2].text

    p_name = driver.find_element(By.CSS_SELECTOR,'._aa_c > span').text
    p_bio = driver.find_elements(By.CSS_SELECTOR,'._aa_c > div')[0].text

def get_feed_url() : 
    global feed_url
    try : 
        for i in range(times):
            a_url = driver.find_elements(By.CSS_SELECTOR,'._ac7v > ._aanf > a')[i+feed-1].get_attribute('href')
            feed_url.append(a_url)
    except :
        print('피드 주소를 얻는데 실패하였습니다.')

def feed_info() :
    global date, whole_text, hashtag
    hashtag = []
    web_source = driver.page_source
    soup = BeautifulSoup(web_source,'lxml')
    date = soup.select('time')[0].attrs['title']
    whole_text = soup.select('._a9zs')[0]
    try :
        whole_tags = whole_text.select('span > a')
        for tag in (whole_tags) :
            hashtag.append(tag.text)
    except :
        print('null')


#=============================================
information()

driver = webdriver.Chrome('/Users/yoon/Desktop/instaPhoto/chromedriver')
driver.get('https://www.instagram.com')
time.sleep(3)

login(id,password)

driver.get(f'https://www.instagram.com/{search_id}')
time.sleep(3)

profile_info()

feed_url = []
get_feed_url()

print(f'{p_img} \n게시물 : {p_post}    팔로워 : {p_follower}    팔로우 : {p_follow}')
print(f'이름 : {p_name}     자기소개 : {p_bio}')

for link in feed_url :
    driver.get(link)
    time.sleep(2)
    feed_info()
    print(f'{date} \n{whole_text.text} \n 해쉬태그 = {hashtag}')

    

