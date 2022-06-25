from gettext import find
from re import I
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time
import urllib.request
import ssl

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

def get_feed_url() : 
    global feed_url
    try : 
        for i in range(times):
            a_url = driver.find_elements(By.CSS_SELECTOR,'._ac7v > ._aanf > a')[i+feed-1].get_attribute('href')
            feed_url.append(a_url)
    except :
        print('피드 주소를 얻는데 실패하였습니다.')

def find_url() :
    global temp
    img=[]
    vid=[]
    while 1:    
        web_source = driver.page_source
        soup = BeautifulSoup(web_source,'lxml')
        #video or photo
        try :
            vedios = soup.select('video')[1]
            if len(vid) == 0 :
                vedios = soup.select('video')[0]
                vid.append('O')
            vedio_src = vedios.attrs['poster']
            temp.append(vedio_src)
        except :
            imgs = soup.select('img')[1]
            if len(img) == 0 :
                imgs = soup.select('img')[0]
                img.append('O')
            img_src=imgs.attrs['src']
            if img_src:
                temp.append(img_src)
            else:
                imgs = imgs.attrs['srcset']
                temp.append(img_src)
        #move to next
        try :
            driver.find_element(By.CLASS_NAME,"_9zm2").click()
            time.sleep(1)
        except NoSuchElementException : 
            break

def img_download(TEMP) :
    ssl._create_default_https_context = ssl._create_unverified_context
    for i, img in enumerate(TEMP) :
        name = f'{search_id}_{feed+count}_{i+1}.png'
        path = f'/Users/yoon/Desktop/Insta/img/{name}'
        urllib.request.urlretrieve(img, path)

#===========================================================

information()
driver = webdriver.Chrome('/Users/yoon/Desktop/instaPhoto/chromedriver')
driver.get('https://www.instagram.com')
time.sleep(2)
login(id,password)

driver.get(f'https://www.instagram.com/{search_id}/')
time.sleep(3)
feed_url=[]
get_feed_url()

count = 0
for link in feed_url :
    temp=[]
    driver.get(link)
    time.sleep(2)
    find_url()
    img_download(temp)
    time.sleep(1)
    count+=1
print("다운로드가 완료되었습니다.")