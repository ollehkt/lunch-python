# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support import expected_conditions as EC
# from fastapi import APIRouter
# from time import sleep
# import pandas as pd

# class Colors:
#     BLUE = '\033[94m'
#     RED = '\033[91m'
#     GREEN = '\033[92m'
#     CYAN = '\033[96m'
#     MAGENTA = '\033[95m'
#     RESET = '\033[0m'

# router = APIRouter(prefix="/naver", tags=["naver"])

# result = pd.DataFrame()

# def switch_left():
#   ############## iframe으로 왼쪽 포커스 맞추기 ##############
#   driver.switch_to.parent_frame()
#   iframe = driver.find_element(By.XPATH,'//*[@id="searchIframe"]')
#   driver.switch_to.frame(iframe)
    
# def switch_right():
#     ############## iframe으로 오른쪽 포커스 맞추기 ##############
#     driver.switch_to.parent_frame()
#     iframe = driver.find_element(By.XPATH,'//*[@id="entryIframe"]')
#     driver.switch_to.frame(iframe)

# options = webdriver.ChromeOptions()
# options.add_argument('window-size=1380,900')
# driver = webdriver.Chrome(options=options)

# # 반복 종료 조건
# loop = True

# # 3초 대기
# driver.implicitly_wait(time_to_wait=3)

# # 네이버 지도 이동
# driver.get("https://map.naver.com/p/search/%EC%9D%8C%EC%8B%9D%EC%A0%90?c=15.00,0,0,0,dh")


# while loop:
#     # 줌 레벨 더하기
#     ## 원하는 대로 작동하지 않던 코드
#         # zoom_in_btn = WebDriverWait(driver, 10).until(
#         #     EC.presence_of_element_located((By.CSS_SELECTOR, ".btn_widget_zoom.zoom_in"))
#         # )
#         # sleep(0.5)  # 0.5초만 기다림
#         # JavaScript로 클릭 실행
#         # driver.execute_script("arguments[0].click();", zoom_in_btn) -> element 가져와서 클릭 실행해도 동작하지 않았음.
#     ## 잘 작동하는 코드
#     # sleep(3)
#     # for i in range(2):
#     #     driver.find_element(By.CSS_SELECTOR, ".btn_widget_zoom.zoom_in").click()
#     #     sleep(1)
   
#     # 왼쪽 포커스 맞추기
#     switch_left()


#     #다음 페이지 버튼 확인
#     next_page = driver.find_element(By.XPATH, '//div[@id="app-root"]/div/div[2]/div[2]/a[7]').get_attribute('aria-disabled')
#     if next_page == 'true':
#         break

#     # 스크롤 가능한 요소 컨테이너 가져오기
#     scrollable_element = driver.find_element(By.CLASS_NAME, "Ryr1F")   


#     # 스크롤 가능한 요소의 최대 높이 가져오기
#     last_height = driver.execute_script("return arguments[0].scrollHeight", scrollable_element)

#     while True:
#         # 스크롤 가능한 요소의 높이를 600만큼 증가
#         driver.execute_script("arguments[0].scrollTop += 600;", scrollable_element)

#         # 동적 스크롤 대기 시간
#         sleep(0.5)

#         # 새로 가져온 스크롤 가능한 요소의 높이
#         new_height = driver.execute_script("return arguments[0].scrollHeight", scrollable_element)

#         # 스크롤 가능한 요소의 높이가 변경되지 않았으면 반복 종료
#         if new_height == last_height:
#             break
#         else:
#             last_height = new_height

#     # 현재 페이지 번호 가져오기
#     page_no = driver.find_element(By.XPATH,'//a[contains(@class, "mBN2s qxokY")]').text

#     # 현재 페이지 번호가 1이면 앞의 2개는 광고라서 광고 빼고 가져오기
#     if page_no == '1':
#         elements = driver.find_elements(By.XPATH,'//*[@id="_pcmap_list_scroll_container"]//li')[2:]
#     else:
#         elements = driver.find_elements(By.XPATH, '//*[@id="_pcmap_list_scroll_container"]//li')

#     print('현재 ' + '\033[95m' + str(page_no) + '\033[0m' + ' 페이지 / '+ '총 ' + '\033[95m' + str(len(elements)) + '\033[0m' + '개의 가게를 찾았습니다.\n')

#     # 가게 정보 가져오기

#     # for index, e in enumerate(elements, start=1):
#     #     final_element = e.find_element(By.CLASS_NAME,'CHC5F').find_element(By.XPATH, ".//a/div/div/span") 
#     #     print(str(index) + ". " + final_element.text)

#     # print("-"*50)

#     switch_left()

#     sleep(2)

#     for index, e in enumerate(elements, start=1):
#         store_name = ''
#         category = ''
#         new_open = ''
#         rating = 0.0
#         visited_review = 0
#         blog_review = 0
#         store_id = ''
#         address = ''
#         business_hours = []
#         phone_num = ''
        
#         switch_left()

#         try:
#             e.find_element(By.CLASS_NAME,'CHC5F').find_element(By.XPATH, ".//a/div/div/span").click()
#             sleep(1)
       

#             switch_right()
#             sleep(1)

#             title = driver.find_element(By.XPATH,'//div[@class="zD5Nm undefined"]')
#             store_info = title.find_elements(By.XPATH,'//div[@class="LylZZ v8v5j"]/div/span')

#             store_name = title.find_element(By.XPATH, './/div[1]/div[1]/span[1]').text
#             category = title.find_element(By.XPATH,'.//div[1]/div[1]/span[2]').text

#             if(len(store_info) > 2):
#                 # 새로 오픈
#                 new_open = title.find_element(By.XPATH,'.//div[1]/div[1]/span[3]').text

#             review = title.find_elements(By.XPATH,'.//div[2]/span')

#             _index = 1

#             if len(review) > 2:
#                 rating_xpath = f'.//div[2]/span[{_index}]'
#                 rating_element = title.find_element(By.XPATH, rating_xpath)
#                 rating = rating_element.text.replace("\n", " ") 
#                 _index += 1

#             try:
#               # 방문자 리뷰
#               visited_review = title.find_element(By.XPATH,f'.//div[2]/span[{_index}]/a').text

#               # 인덱스를 다시 +1 증가 시킴
#               _index += 1

#               # 블로그 리뷰
#               blog_review = title.find_element(By.XPATH,f'.//div[2]/span[{_index}]/a').text
#             except:
#               print(Colors.RED + '------------ 리뷰 부분 오류 ------------' + Colors.RESET)

#             try:
#                 store_id = title.find_element(By.XPATH,'.//div[2]/span[2]/a').get_attribute('href').split('/')[4]
#             except:
#                 print(Colors.RED + '------------ store_id 추출 오류 ------------' + Colors.RESET)
#             try:
#                 address = driver.find_element(By.XPATH,'//span[@class="LDgIH"]').text
#             except:
#                 print(Colors.RED + '------------ 주소 추출 오류 ------------' + Colors.RESET)

#             try:
#                 driver.find_element(By.XPATH,'//div[@class="O8qbU pSavy"]/div/a/div[1]/div').click()
#                 # 영업 시간 더보기 버튼을 누르고 2초 반영시간 기다림
#                 sleep(2)

#                 parent_element = driver.find_element(By.XPATH,'//a[@class="gKP9i RMgN0"]')
#                 child_elements = parent_element.find_elements(By.XPATH, './*[@class="w9QyJ" or @class="w9QyJ undefined"]')

#                 for child in child_elements:
#                     # 각 자식 요소 내에서 클래스가 'A_cdD'인 span 요소 찾기
#                     span_elements = child.find_elements(By.XPATH, './/span[@class="A_cdD"]')

#                     # 찾은 span 요소들의 텍스트 출력
#                     for span in span_elements:
#                         business_hours.append(span)
                
#                 # 가게 전화번호
#                 phone_num = driver.find_element(By.XPATH,'//span[@class="xlx7Q"]').text

#             except:
#               print(Colors.RED + '------------ 영업시간 / 전화번호 부분 오류 ------------' + Colors.RESET)
#         except:
#             print(Colors.RED + '------------ 가게 정보 오류 ------------' + Colors.RESET) 

#         # print(Colors.BLUE + f'{index}. ' + str(store_name) + Colors.RESET + ' · ' + str(category) + Colors.RED + str(new_open) + Colors.RESET)
#         # print('평점 ' + Colors.RED + str(rating) + Colors.RESET + ' / ' + visited_review + ' · ' + blog_review)
#         # print(f'가게 고유 번호 -> {store_id}')
#         # print('가게 주소 ' + Colors.GREEN + str(address) + Colors.RESET)
#         # print(Colors.CYAN + '가게 영업 시간' + Colors.RESET)
#         # for i in business_hours:
#         #     print(i.text)
#         #     print('')
#         # print('가게 번호 ' + Colors.GREEN + phone_num + Colors.RESET)
#         # print(Colors.MAGENTA + "-"*50 + Colors.RESET)

#         result = pd.concat([result, pd.DataFrame({
#             'store_name': [store_name],
#             'category': [category],
#             'new_open': [new_open],
#             'rating': [rating],
#             'visited_review': [visited_review],
#             'blog_review': [blog_review],
#             'store_id': [store_id],
#             'address': [address],
#             'business_hours': [business_hours],
#             'phone_num': [phone_num]
#         })])

#     if next_page == 'false':
#           driver.find_element(By.XPATH,'//div[@id="app-root"]/div/div[2]/div[2]/a[7]').click()
#       # 아닐 경우 루프 정지
#     else:
#         loop = False

# result.to_csv('./result.csv', index=False)


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from fastapi import APIRouter
from time import sleep
import pandas as pd

class Colors:
    BLUE = '\033[94m'
    RED = '\033[91m'
    GREEN = '\033[92m'
    CYAN = '\033[96m'
    MAGENTA = '\033[95m'
    RESET = '\033[0m'

router = APIRouter(prefix="/naver", tags=["naver"])

# API 엔드포인트 추가
@router.get("/scrape",name="네이버 지도 크롤링 데이터 수집 API",responses={200: {"description": "요청 성공", "content": {
    "application/json": {
        "example": {
            "status": "success",
            "message": "데이터 수집 완료"
        }
    }
}}, 403: {"description": "네이버 맵 크롤링 중 오류가 발생했습니다."},500: {"description": "알 수 없는 오류가 발생했습니다."}})

async def start_scraping():
    # 백그라운드 작업으로 실행하는 것이 좋지만, 간단한 예시로 직접 호출
    try:
        scrape_naver_map()
        return {"status": "success", "message": "데이터 수집 완료"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

result = pd.DataFrame()

def scrape_naver_map():
    options = webdriver.ChromeOptions()
    options.add_argument('window-size=1380,900')
    driver = webdriver.Chrome(options=options)

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
    
    # 3초 대기
    driver.implicitly_wait(time_to_wait=3)
    
    # 네이버 지도 이동
    driver.get("https://map.naver.com/p/search/%EC%9D%8C%EC%8B%9D%EC%A0%90?c=15.00,0,0,0,dh")
    
    # 페이지 로딩 대기
    sleep(5)
    
    # 결과 저장용 DataFrame
    result = pd.DataFrame()
    
    # 반복 종료 조건
    loop = True
    
    while loop:
        try:
            # 왼쪽 포커스 맞추기
            switch_left()
            
            # 다음 페이지 버튼 확인 - 더 안정적인 방법으로 변경
            try:
                next_page = driver.find_element(By.XPATH, '//div[@id="app-root"]/div/div[2]/div[2]/a[7]').get_attribute('aria-disabled')
                next_page_btn = driver.find_element(By.XPATH, '//div[@id="app-root"]/div/div[2]/div[2]/a[7]')
                if next_page == 'true':
                    break
            except:
                print("다음 페이지 버튼을 찾을 수 없습니다.")
                
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

                # 스크롤 가능한 요소의 높이가 변경되지 않았으면 반복 종료
                if new_height == last_height:
                    break
                else:
                    last_height = new_height

            # 현재 페이지 번호 가져오기
            page_no = driver.find_element(By.XPATH,'//a[contains(@class, "mBN2s qxokY")]').text

            # 현재 페이지 번호가 1이면 앞의 2개는 광고라서 광고 빼고 가져오기
            if page_no == '1':
                elements = driver.find_elements(By.XPATH,'//*[@id="_pcmap_list_scroll_container"]//li')[2:]
            else:
                elements = driver.find_elements(By.XPATH, '//*[@id="_pcmap_list_scroll_container"]//li')

            print('현재 ' + '\033[95m' + str(page_no) + '\033[0m' + ' 페이지 / '+ '총 ' + '\033[95m' + str(len(elements)) + '\033[0m' + '개의 가게를 찾았습니다.\n')

            # 가게 정보 가져오기

            # for index, e in enumerate(elements, start=1):
            #     final_element = e.find_element(By.CLASS_NAME,'CHC5F').find_element(By.XPATH, ".//a/div/div/span") 
            #     print(str(index) + ". " + final_element.text)

            # print("-"*50)

            switch_left()

            sleep(2)

            for index, e in enumerate(elements, start=1):
                store_name = '없음'
                category = '없음'
                new_open = '없음'
                rating = 0.0
                visited_review = 0
                blog_review = 0
                store_id = '없음'
                address = '없음'
                business_hours = ''
                phone_num = '없음'
                lat_lng = ''
                
                switch_left()

                try:
                    e.find_element(By.CLASS_NAME,'CHC5F').find_element(By.XPATH, ".//a/div/div/span").click()
                    sleep(1)
                    url_query = e.find_element(By.CLASS_NAME,'CHC5F').find_element(By.XPATH, ".//a").get_attribute('href')
                    x = url_query.split('clientX=')[1].split('&')[0]
                    y = url_query.split('clientY=')[1].split('&')[0]
                    lat_lng = {
                        'x': x,
                        'y': y
                    }

                    switch_right()
                    sleep(2)

                    title = driver.find_element(By.XPATH,'//div[@class="zD5Nm undefined"]')
                    store_info = title.find_elements(By.XPATH,'//div[@class="LylZZ v8v5j"]/div/span')

                    store_name = title.find_element(By.XPATH, './/div[1]/div[1]/span[1]').text
                    category = title.find_element(By.XPATH,'.//div[1]/div[1]/span[2]').text

                    if(len(store_info) > 2):
                        # 새로 오픈
                        new_open = title.find_element(By.XPATH,'.//div[1]/div[1]/span[3]').text

                    review = title.find_elements(By.XPATH,'.//div[2]/span')

                    _index = 1

                    if len(review) > 2:
                        rating_xpath = f'.//div[2]/span[{_index}]'
                        rating_element = title.find_element(By.XPATH, rating_xpath)
                        rating = rating_element.text.replace("\n", " ").replace('별점 ','')
                        _index += 1

                    try:
                        # 방문자 리뷰
                        visited_review = title.find_element(By.XPATH,f'.//div[2]/span[{_index}]/a').text.replace('방문자 리뷰 ','')

                        # 인덱스를 다시 +1 증가 시킴
                        _index += 1

                        # 블로그 리뷰
                        blog_review = title.find_element(By.XPATH,f'.//div[2]/span[{_index}]/a').text.replace('블로그 리뷰 ','')
                    except:
                        print(Colors.RED + '------------ 리뷰 부분 오류 ------------' + Colors.RESET)

                    try:
                        store_id = title.find_element(By.XPATH,'.//div[2]/span[2]/a').get_attribute('href').split('/')[4]
                    except:
                        print(Colors.RED + '------------ store_id 추출 오류 ------------' + Colors.RESET)
                    try:
                        address = driver.find_element(By.XPATH,'//span[@class="LDgIH"]').text
                    except:
                        print(Colors.RED + '------------ 주소 추출 오류 ------------' + Colors.RESET)

                    try:
                        driver.find_element(By.XPATH,'//div[@class="O8qbU pSavy"]/div/a/div[1]/div').click()
                        # 영업 시간 더보기 버튼을 누르고 2초 반영시간 기다림
                        sleep(2)

                        parent_element = driver.find_element(By.XPATH,'//a[@class="gKP9i RMgN0"]')
                        child_elements = parent_element.find_elements(By.XPATH, './*[@class="w9QyJ" or @class="w9QyJ undefined"]')

                        for child in child_elements:
                            # 각 자식 요소 내에서 클래스가 'A_cdD'인 span 요소 찾기
                            span_elements = child.find_elements(By.XPATH, './/span[@class="A_cdD"]')

                            # 찾은 span 요소들의 텍스트 출력
                            for span in span_elements:
                                business_hours += f'{span.text} /'
                        
                        # 가게 전화번호
                        phone_num = driver.find_element(By.XPATH,'//span[@class="xlx7Q"]').text

                    except:
                      print(Colors.RED + '------------ 영업시간 / 전화번호 부분 오류 ------------' + Colors.RESET)
                except:
                    print(Colors.RED + '------------ 가게 정보 오류 ------------' + Colors.RESET) 

                result = pd.concat([result, pd.DataFrame({
                    'store_name': [store_name],
                    'category': [category],
                    'new_open': [new_open],
                    'rating': [str(rating)],
                    'visited_review': [visited_review],
                    'blog_review': [blog_review],
                    'store_id': [store_id],
                    'address': [address],
                    'business_hours': [business_hours],
                    'phone_num': [phone_num],
                    'lat_lng': [lat_lng]
                })])

            switch_left()
            sleep(2)
            
            if next_page == 'false':
                next_page_btn.click()
                sleep(2)
            else:
                loop = False

        except Exception as e:
            print(f"오류 발생: {str(e)}")
            break
            
    # 결과 저장
    result.to_csv('./result.csv', index=False)
    
    # 브라우저 종료
    driver.quit()

