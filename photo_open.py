from gettext import find
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

def login(id,password) :
    a = driver.find_elements(By.CLASS_NAME,'_2hvTZ')[0] #id input tag class
    a.send_keys(id)

    a = driver.find_elements(By.CLASS_NAME,'_2hvTZ')[1] #password input tag class
    a.send_keys(password)
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
    web_source = driver.page_source
    soup = BeautifulSoup(web_source,'lxml')
    #비디오
    try :
        vedio = driver.find_element(By.CLASS_NAME,'_ab1d')
        vedio_src = vedio.get_attribute('poster')
        temp.append(vedio_src)
    #이미지
    except NoSuchElementException :
        #첫번째 사진
        imgs = soup.select('img')[0]
        img_src=imgs.attrs['src']
        if img_src:
            temp.append(img_src)
        else:
            img_src = imgs.attrs['srcset']
            temp.append(img_src)
        #이후 사진
        while 1 :
            try :
                driver.find_element(By.CLASS_NAME,"_9zm2").click()
                time.sleep(1)
                web_source = driver.page_source
                soup = BeautifulSoup(web_source,'lxml')
                imgs = soup.select('img')[1]
                imgs=imgs.attrs['src']
                if imgs:
                    temp.append(imgs)
                else:
                    imgs = imgs.attrs['srcset']
                    temp.append(imgs)
            except NoSuchElementException :
                break 

def window_new_tap(temp) :
    for i in temp :
        driver.execute_script(f'window.open("{i}");')
    driver.switch_to.window(driver.window_handles[0])
    time.sleep(1)

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

for link in feed_url :
    temp=[]
    driver.get(link)
    time.sleep(2)
    find_url()
    window_new_tap(temp)
    print(temp)
print("==================================================================================")