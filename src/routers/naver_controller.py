from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from fastapi import APIRouter, HTTPException
from time import sleep
import random
import re

router = APIRouter(prefix="/naver", tags=["naver"])


def switch_left():
  ############## iframe으로 왼쪽 포커스 맞추기 ##############
  driver.switch_to.parent_frame()
  iframe = driver.find_element(By.XPATH,'//*[@id="searchIframe"]')
  driver.switch_to.frame(iframe)
    
def switch_right():
    ############## iframe으로 오른쪽 포커스 맞추기 ##############
    driver.switch_to.parent_frame()
    iframe = driver.find_element(By.XPATH,'//*[@id="entryIframe"]')
    driver.switch_to.frame(iframe)

options = webdriver.ChromeOptions()
options.add_argument('window-size=1380,900')
driver = webdriver.Chrome(options=options)

# 반복 종료 조건
loop = True

# 3초 대기
driver.implicitly_wait(time_to_wait=3)

# 네이버 지도 이동
driver.get("https://map.naver.com/p/search/%EC%9D%8C%EC%8B%9D%EC%A0%90?c=15.00,0,0,0,dh")


while loop:
  
    # 줌 레벨 더하기
    ## 원하는 대로 작동하지 않던 코드
        # zoom_in_btn = WebDriverWait(driver, 10).until(
        #     EC.presence_of_element_located((By.CSS_SELECTOR, ".btn_widget_zoom.zoom_in"))
        # )
        # sleep(0.5)  # 0.5초만 기다림
        # JavaScript로 클릭 실행
        # driver.execute_script("arguments[0].click();", zoom_in_btn) -> element 가져와서 클릭 실행해도 동작하지 않았음.
    ## 잘 작동하는 코드
    sleep(3)
    for i in range(2):
        driver.find_element(By.CSS_SELECTOR, ".btn_widget_zoom.zoom_in").click()
        sleep(1)
   
    # 왼쪽 포커스 맞추기
    switch_left()


    #다음 페이지 버튼 확인
    next_page = driver.find_element(By.XPATH, '//div[@id="app-root"]/div/div[2]/div[2]/a[7]').get_attribute('aria-disabled')
    if next_page == 'true':
        break

    # 스크롤 가능한 요소 컨테이너 가져오기
    scrollable_element = driver.find_element(By.CLASS_NAME, "Ryr1F")   


    # 스크롤 가능한 요소의 최대 높이 가져오기
    last_height = driver.execute_script("return arguments[0].scrollHeight", scrollable_element)

    while True:
        # 스크롤 가능한 요소의 높이를 600만큼 증가
        driver.execute_script("arguments[0].scrollTop += 600;", scrollable_element)

        # 동적 스크롤 대기 시간
        sleep(0.5)

        # 새로 가져온 스크롤 가능한 요소의 높이
        new_height = driver.execute_script("return arguments[0].scrollHeight", scrollable_element)

        print(new_height)
        # 스크롤 가능한 요소의 높이가 변경되지 않았으면 반복 종료
        if new_height == last_height:
            break
        else:
            last_height = new_height

    # 현재 페이지 번호 가져오기
    page_no = driver.find_element(By.XPATH,'//a[contains(@class, "mBN2s qxokY")]').text
    print(page_no)

    # 현재 페이지 번호가 1이면 앞의 2개는 광고라서 광고 빼고 가져오기
    if page_no == '1':
        elements = driver.find_elements(By.XPATH,'//*[@id="_pcmap_list_scroll_container"]//li')[2:]
    else:
        elements = driver.find_elements(By.XPATH, '//*[@id="_pcmap_list_scroll_container"]//li')

    print('현재 ' + '\033[95m' + str(page_no) + '\033[0m' + ' 페이지 / '+ '총 ' + '\033[95m' + str(len(elements)) + '\033[0m' + '개의 가게를 찾았습니다.\n')

    # 가게 정보 가져오기

    loop = False
