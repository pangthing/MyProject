import json
import urllib
from urllib.request import Request, urlopen
# *-- 3개의 주소 geocoding으로 변환한다.(출발지, 도착지, 경유지) --*
# start = '경기도 용인시 기흥구 하갈동 1-1'
# goal = '경기도 수원시 영통구 영통동 992-13'
# waypoint = '경기도 수원시 장안구 서부로 2149'

# 주소에 geocoding 적용하는 함수를 작성.
def get_location(loc) :
    client_id = 'un9kcwrg1q'
    client_secret = 'siQivhiLqX0w2R6BVyYV2Z6HHbvk3nsh66K3jLtu'
    url = f"https://naveropenapi.apigw.ntruss.com/map-geocode/v2/geocode?query=" \
    			+ urllib.parse.quote(loc)
    
    # 주소 변환
    request = urllib.request.Request(url)
    request.add_header('X-NCP-APIGW-API-KEY-ID', client_id)
    request.add_header('X-NCP-APIGW-API-KEY', client_secret)
    
    response = urlopen(request)
    res = response.getcode()
    
    if (res == 200) : # 응답이 정상적으로 완료되면 200을 return한다
        response_body = response.read().decode('utf-8')
        response_body = json.loads(response_body)
        print(response_body)
        # 주소가 존재할 경우 total count == 1이 반환됨.
        if response_body['meta']['totalCount'] == 1 : 
        	# 위도, 경도 좌표를 받아와서 return해 줌.
            lat = response_body['addresses'][0]['y']
            lon = response_body['addresses'][0]['x']
            return (lon, lat)
        else :
            print('location not exist')
        
    else :
        print('ERROR')

def get_optimal_route(start, goal, waypoints=['',''], option='') :
    client_id = 'un9kcwrg1q'
    client_secret = 'siQivhiLqX0w2R6BVyYV2Z6HHbvk3nsh66K3jLtu' 
    # start=/goal=/(waypoint=)/(option=) 순으로 request parameter 지정
    url = f"https://naveropenapi.apigw.ntruss.com/map-direction-15/v1/driving?start={start[0]},{start[1]}&goal={goal[0]},{goal[1]}&option={option}"
    request = urllib.request.Request(url)
    request.add_header('X-NCP-APIGW-API-KEY-ID', client_id)
    request.add_header('X-NCP-APIGW-API-KEY', client_secret)
    
    response = urllib.request.urlopen(request)
    res = response.getcode()
    
    if (res == 200) :
        response_body = response.read().decode('utf-8')
        return json.loads(response_body)
            
    else :
        print('ERROR')

#  함수 적용
if __name__ == "__main__":
    
    start = '경기도 용인시 기흥구 하갈동 1-1'
    goal = '경기도 수원시 영통구 영통동 992-13'

    start = get_location(start)
    goal = get_location(goal)

    print(start)
    print(goal)

    results = get_optimal_route(start, goal, option='')
    print(results['route']['traoptimal'][0]['path'])
# waypoint = get_location(waypoint)
