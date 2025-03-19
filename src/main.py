import uvicorn
import os
import requests
from dotenv import load_dotenv
import random
from fastapi import FastAPI, HTTPException
from typing import Optional
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd

from src.routers.naver_controller import router as naver_router

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(naver_router)

@app.get("/")
def read_root():
    return {"message": "Hello World"}

if __name__ == "__main__":
    uvicorn.run("src.main:app", host="0.0.0.0", port=8000, reload=True)

@app.get('/restaurants/random/{x}/{y}',name="카카오 맵 API 호출 및 랜덤 데이터 반환 API",responses={200: {"description": "요청 성공", "content": {
    "application/json": {
        "example": {
            "choice": {
                "address_name": "서울 강남구 논현동 114-28",
                "category_group_code": "FD6",
                "category_group_name": "음식점",
                "category_name": "음식점 > 술집 > 호프,요리주점 > 펀비어킹",
                "distance": "43",
                "id": "26772671",
                "phone": "02-544-5354",
                "place_name": "펀비어킹 강남세관사거리점",
                "place_url": "http://place.map.kakao.com/26772671",
                "road_address_name": "서울 강남구 언주로134길 19",
                "x": "127.037174177028",
                "y": "37.5169499483626"
            },
            "total_count": 15,
            "restaurant_list": [
                {
                    "address_name": "서울 강남구 논현동 114-28",
                    "category_group_code": "FD6",
                    "category_group_name": "음식점",
                    "category_name": "음식점 > 술집 > 호프,요리주점 > 펀비어킹",
                    "distance": "43",
                    "id": "26772671",
                    "phone": "02-544-5354",
                    "place_name": "펀비어킹 강남세관사거리점",
                    "place_url": "http://place.map.kakao.com/26772671",
                    "road_address_name": "서울 강남구 언주로134길 19",
                    "x": "127.037174177028",
                    "y": "37.5169499483626"
                }
            ]
        }
    }   
}}, 403: {"description": "카카오 맵 API 호출 중 오류가 발생했습니다."},500: {"description": "알 수 없는 오류가 발생했습니다."}})
async def get_restaurants_list_and_random_place(x: float = 127.04036572242, y: float = 37.510168764968
, kind: Optional[str] = None) -> dict:
    """
    주변 음식점 목록을 조회하고 랜덤으로 하나를 선택합니다. \n
    파라미터에 들어가는 x, y 기본 값은 선릉로111길 40 주소의 위도 경도 입니다.

    Parameters:
    
        - x (float): 경도 좌표 (Longitude). 기본값: 127.04036572242
        - y (float): 위도 좌표 (Latitude). 기본값: 37.510168764968
        - kind (Optional[str]): 음식점 분류 (예: 중식, 일식, 한식 등). 기본값: None
    """
    load_dotenv(os.path.join(os.path.dirname(__file__), ".env"), override=True)
    try:
        restaurant_list = []
        api_key = os.environ.get('KAKAO_MAP_API_KEY')
        if not api_key:
            return {"error": "KAKAO_MAP_API_KEY가 설정되지 않았습니다"}

        url = "https://dapi.kakao.com/v2/local/search/category.json"
        params = {
            "category_group_code": "FD6",  # 음식점 카테고리
            "x": x,
            "y": y,
            "radius": 500,  # 500m 반경
            "sort": "distance",
            "page": 1
        }
        headers = {
            "Authorization": f"KakaoAK {api_key}",
            "Content-Type": "application/json"
        }
        
        response = requests.get(url, headers=headers, params=params).json()
        if(response == None):
            raise HTTPException(status_code=403, detail="카카오 맵 API 호출 중 오류가 발생했습니다.")
        total_pages = min(3, (response['meta']["pageable_count"] + 14) // 15)
        # a_list =  [{'address_name': '서울 강남구 논현동 114-28', 'category_group_code': 'FD6', 'category_group_name': '음식점', 'category_name': '음식점 > 술집 > 호프,요리주점 > 펀비어킹', 'distance': '43', 'id': '26772671', 'phone': '02-544-5354', 'place_name': '펀비어킹 강남세관사거리점', 'place_url': 'http://place.map.kakao.com/26772671', 'road_address_name': '서울 강남구 언주로134길 19', 'x': '127.037174177028', 'y': '37.5169499483626'}, {'address_name': '서울 강남구 논현동 114-27', 'category_group_code': 'FD6', 'category_group_name': '음식점', 'category_name': '음식점 > 한식', 'distance': '49', 'id': '8188651', 'phone': '02-543-6363', 'place_name': '고향집', 'place_url': 'http://place.map.kakao.com/8188651', 'road_address_name': '서울 강남구 언주로134길 17', 'x': '127.03701128228153', 'y': '37.51693197944849'}, {'address_name': '서울 강남구 논현동 113-17', 'category_group_code': 'FD6', 'category_group_name': '음식점', 'category_name': '음식점 > 도시락 > 한솥도시락', 'distance': '52', 'id': '11634446', 'phone': '02-541-6211', 'place_name': '한솥도시락 관세청앞점', 'place_url': 'http://place.map.kakao.com/11634446', 'road_address_name': '서울 강남구 언주로134길 25', 'x': '127.037644768726', 'y': '37.517014671566'}, {'address_name': '서울 강남구 논현동 113-17', 'category_group_code': 'FD6', 'category_group_name': '음식점', 'category_name': '음식점 > 한식 > 국밥', 'distance': '57', 'id': '532632180', 'phone': '02-3446-6699', 'place_name': '콩뿌리콩나물국밥 강남구청점', 'place_url': 'http://place.map.kakao.com/532632180', 'road_address_name': '서울 강남구 언주로134길 25', 'x': '127.03771489701808', 'y': '37.517008342169916'}, {'address_name': '서울 강남구 논현동 114-26', 'category_group_code': 'FD6', 'category_group_name': '음식점', 'category_name': '음식점 > 중식 > 양꼬치 > 이가네양꼬치', 'distance': '58', 'id': '1937749932', 'phone': '02-518-1812', 'place_name': '이가네양꼬치 강남구청점', 'place_url': 'http://place.map.kakao.com/1937749932', 'road_address_name': '서울 강남구 언주로134길 15', 'x': '127.036864214865', 'y': '37.5168959852942'}, {'address_name': '서울 강남구 논현동 108-3', 'category_group_code': 'FD6', 'category_group_name': '음식점', 'category_name': '음식점 > 한식 > 육류,고기 > 닭요리', 'distance': '60', 'id': '376473135', 'phone': '070-8680-3270', 'place_name': '강남계집', 'place_url': 'http://place.map.kakao.com/376473135', 'road_address_name': '서울 강남구 언주로136길 27', 'x': '127.037724293215', 'y': '37.5176976067865'}, {'address_name': '서울 강남구 논현동 114-18', 'category_group_code': 'FD6', 'category_group_name': '음식점', 'category_name': '음식점 > 술집 > 호프,요리주점', 'distance': '64', 'id': '301261966', 'phone': '', 'place_name': '바벤술', 'place_url': 'http://place.map.kakao.com/301261966', 'road_address_name': '서울 강남구 언주로134길 11-5', 'x': '127.036539679992', 'y': '37.5171123269792'}, {'address_name': '서울 강남구 논현동 113-25', 'category_group_code': 'FD6', 'category_group_name': '음식점', 'category_name': '음식점 > 한식', 'distance': '68', 'id': '585589573', 'phone': '', 'place_name': '팔당푸드', 'place_url': 'http://place.map.kakao.com/585589573', 'road_address_name': '서울 강남구 언주로134길 29', 'x': '127.037925336541', 'y': '37.5170974741305'}, {'address_name': '서울 강남구 논현동 114-25', 'category_group_code': 'FD6', 'category_group_name': '음식점', 'category_name': '음식점 > 한식', 'distance': '68', 'id': '1453552771', 'phone': '', 'place_name': '먼치하우스', 'place_url': 'http://place.map.kakao.com/1453552771', 'road_address_name': '서울 강남구 언주로134길 13', 'x': '127.036721673957', 'y': '37.5168635935771'}, {'address_name': '서울 강남구 논현동 113-25', 'category_group_code': 'FD6', 'category_group_name': '음식점', 'category_name': '음식점 > 한식 > 국수', 'distance': '69', 'id': '23825025', 'phone': '02-3445-4686', 'place_name': '팔당충무김밥국수', 'place_url': 'http://place.map.kakao.com/23825025', 'road_address_name': '서울 강남구 언주로134길 29', 'x': '127.037925327421', 'y': '37.5170794540642'}, {'address_name': '서울 강남구 논현동 114-25', 'category_group_code': 'FD6', 'category_group_name': '음식점', 'category_name': '음식점 > 치킨 > 가마치통닭', 'distance': '69', 'id': '1830668748', 'phone': '02-543-7848', 'place_name': '가마치통닭 강남구청역점', 'place_url': 'http://place.map.kakao.com/1830668748', 'road_address_name': '서울 강남구 언주로134길 13', 'x': '127.03671714758953', 'y': '37.51685999096337'}, {'address_name': '서울 강남구 논현동 116-1', 'category_group_code': 'FD6', 'category_group_name': '음식점', 'category_name': '음식점 > 양식', 'distance': '69', 'id': '1045539408', 'phone': '', 'place_name': '라몬', 'place_url': 'http://place.map.kakao.com/1045539408', 'road_address_name': '서울 강남구 언주로134길 24', 'x': '127.037591491559', 'y': '37.5167894376547'}, {'address_name': '서울 강남구 논현동 113-25', 'category_group_code': 'FD6', 'category_group_name': '음식점', 'category_name': '음식점 > 한식', 'distance': '69', 'id': '1593349215', 'phone': '0503-7150-6019', 'place_name': '짐승고깃간', 'place_url': 'http://place.map.kakao.com/1593349215', 'road_address_name': '서울 강남구 언주로134길 29', 'x': '127.037934378475', 'y': '37.5170830551715'}, {'address_name': '서울 강남구 논현동 114-25', 'category_group_code': 'FD6', 'category_group_name': '음식점', 'category_name': '음식점 > 한식 > 육류,고기', 'distance': '69', 'id': '419923613', 'phone': '02-518-6908', 'place_name': '땅코참숯구이 논현직영점', 'place_url': 'http://place.map.kakao.com/419923613', 'road_address_name': '서울 강남구 언주로134길 13', 'x': '127.036735237162', 'y': '37.5168419652755'}, {'address_name': '서울 강남구 논현동 114-19', 'category_group_code': 'FD6', 'category_group_name': '음식점', 'category_name': '음식점 > 양식 > 피자 > 피자탑', 'distance': '70', 'id': '1236855031', 'phone': '02-3443-9909', 'place_name': '피자탑 강남1호점', 'place_url': 'http://place.map.kakao.com/1236855031', 'road_address_name': '서울 강남구 언주로134길 11-3', 'x': '127.036540758426', 'y': '37.5170042062292'}]
        for i in range(1, total_pages):
            params["page"] = i
            res = requests.get(url, headers=headers, params=params).json()
            restaurants = res['documents']


            if kind: 
                filtered_list = list(filter(lambda x: len(x['category_name'].split('>')) > 1 and x['category_name'].split('>')[1].strip() == kind, restaurants))
                restaurant_list.extend(filtered_list)
            else:
                filtered_list = list(filter(lambda x: len(x['category_name'].split('>')) > 1 and x['category_name'].split('>')[1].strip() != '술집', restaurants))
                restaurant_list.extend(filtered_list)


        random_restaurant = random.choice(restaurant_list)

    except Exception as e:
        print(f"Error: {str(e)}")
        raise HTTPException(status_code=500, detail="알 수 없는 오류가 발생했습니다.")

    return {"choice": random_restaurant, "total_count": len(restaurant_list), "restaurant_list": restaurant_list}


@app.get('/restaurants/naver/random')
def get_restaurants_naver_random():
    try:
        df = pd.read_csv('./result.csv')
        try:
            result = format_retaurant_data(df.to_dict("records"))
        except Exception as e:
            raise HTTPException(status_code=500, detail="포맷에서 오류가 발생했습니다.")
        
        random_restaurant = random.choice(result)
        return random_restaurant
    except Exception as e:
        print(f"Error: {str(e)}")
        raise HTTPException(status_code=500, detail="알 수 없는 오류가 발생했습니다.")


@app.get('/restaurants/naver/hanam',name="네이버 지도 크롤링 데이터 반환 API",responses={200: {"description": "요청 성공", "content": {
    "application/json": {
        "example": {
            "total_count": 15,
            "restaurants": [
                {
                    "id": "26772671",
                    "name": "펀비어킹 강남세관사거리점",
                    "category": "음식점 > 술집 > 호프,요리주점 > 펀비어킹",
                    "rating": "4.5",
                    "reviews": {
                        "visitor": "100",
                        "blog": "100"
                    },
                    "address": "서울 강남구 논현동 114-28",
                    "business_hours": {
                        "월요일": ["10:00-20:00"],
                        "화요일": ["10:00-20:00"],
                        "수요일": ["10:00-20:00"],
                        "목요일": ["10:00-20:00"],
                        "금요일": ["10:00-20:00"],
                        "토요일": ["10:00-20:00"],
                        "일요일": ["10:00-20:00"]
                    },
                    "phone": "02-544-5354",
                    "lat_lng": {"x": "127.037174177028", "y": "37.5169499483626"}
                }
            ]
        }
    }
}}, 403: {"description": "네이버 맵 크롤링 중 오류가 발생했습니다."},500: {"description": "알 수 없는 오류가 발생했습니다."}})
def get_restaurants_naver(category: str = None, page: int = 1,page_size: int = 20):
    try:
        
        df = pd.read_csv('./hanam_result.csv')

        if category:
            df = df[df['category'] == category]

        start_idx = (page - 1) * page_size
        end_idx = start_idx + page_size

        try:
            result = format_retaurant_data(df[start_idx:end_idx].to_dict("records"))
        except Exception as e:
            raise HTTPException(status_code=500, detail="포맷에서 오류가 발생했습니다.")

        return {
            "total_count": len(result),
            "restaurants": result
        }

    except Exception as e:
        print(f"Error: {str(e)}")
        raise HTTPException(status_code=500, detail="알 수 없는 오류가 발생했습니다.")

@app.get('/restaurants/naver/company',name="네이버 지도 크롤링 데이터 반환 API",responses={200: {"description": "요청 성공", "content": {
    "application/json": {
        "example": {
            "total_count": 15,
            "restaurants": [
                {
                    "id": "26772671",
                    "name": "펀비어킹 강남세관사거리점",
                    "category": "음식점 > 술집 > 호프,요리주점 > 펀비어킹",
                    "rating": "4.5",
                    "reviews": {
                        "visitor": "100",
                        "blog": "100"
                    },
                    "address": "서울 강남구 논현동 114-28",
                    "business_hours": {
                        "월요일": ["10:00-20:00"],
                        "화요일": ["10:00-20:00"],
                        "수요일": ["10:00-20:00"],
                        "목요일": ["10:00-20:00"],
                        "금요일": ["10:00-20:00"],
                        "토요일": ["10:00-20:00"],
                        "일요일": ["10:00-20:00"]
                    },
                    "phone": "02-544-5354",
                    "lat_lng": {"x": "127.037174177028", "y": "37.5169499483626"}
                }
            ]
        }
    }
}}, 403: {"description": "네이버 맵 크롤링 중 오류가 발생했습니다."},500: {"description": "알 수 없는 오류가 발생했습니다."}})
def get_restaurants_naver(category: str = None, page: int = 1,page_size: int = 20):
    try:
        
        df = pd.read_csv('./company_result.csv')

        if category:
            df = df[df['category'] == category]

        start_idx = (page - 1) * page_size
        end_idx = start_idx + page_size

        try:
            result = format_retaurant_data(df[start_idx:end_idx].to_dict("records"))
        except Exception as e:
            raise HTTPException(status_code=500, detail="포맷에서 오류가 발생했습니다.")

        return {
            "total_count": len(result),
            "restaurants": result
        }

    except Exception as e:
        print(f"Error: {str(e)}")
        raise HTTPException(status_code=500, detail="알 수 없는 오류가 발생했습니다.")

def format_retaurant_data(csv_data):
    restaurants  = []

    for row in csv_data:
        # 빈 데이터 행 제외
        if not row['store_name']:
            continue

        # 영업 시간 정리
        business_hours = {}

        if row['business_hours']:
            days = row['business_hours'].split('/')
            for day in days:
                if not day.strip():
                    continue
                day_info = day.strip().split('\n')
                day_name = day_info[0].strip()
                hours = [h.strip() for h in day_info[1:]]
                business_hours[day_name] = hours
        
        visited_review = row['visited_review'] if row['visited_review'] else '0'
        blog_review = row['blog_review'] if row['blog_review'] else '0'
        rating = row['rating'] if row['rating'] else '0.0'
        lat_lng = eval(row['lat_lng']) if row['lat_lng'] else ''

        restaurant = {
            'id': row['store_id'],
            'name': row['store_name'],
            'category': row['category'],
            'rating': rating,
            'reviews': {
                'visitor': visited_review,
                'blog': blog_review
            },
            'address': row['address'],
            'business_hours': business_hours,
            'phone': row['phone_num'],
            'lat_lng': lat_lng
        }
        restaurants.append(restaurant)

    return restaurants
