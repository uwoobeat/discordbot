import json
import requests

def save_info_from_solvedac(handle): #솔브닥으로부터 참가자 정보 받아서 json으로 저장
    url = "https://solved.ac/api/v3/user/show"
    querystring = {"handle":f"{handle}"}
    headers = {"Content-Type": "application/json"}
    response = requests.request("GET", url, headers=headers, params=querystring).json() #response 객체를 json으로 반환
    try:
        print(f"{handle} 쓰기 시작")
        with open(f"userdata/profile_{handle}.json", 'w', encoding='utf-8') as userdata:
            #### 현재 이 구간에서 문제 발생 중 ####
            
            json.dump(response, userdata, indent=4) #json 파일 쓰기
        print(f"{handle} 쓰기 종료")
        userdata.close()
        return True 
    except:
        return False #성공하면 True, 실패하면 False 반환

save_info_from_solvedac("uwoobeat")