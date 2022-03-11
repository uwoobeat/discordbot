import requests
import json

def save_info_from_solvedac(handle): #솔브닥으로부터 참가자 정보 받아서 json으로 저장
    url = "https://solved.ac/api/v3/user/show"
    querystring = {"handle":f"{handle}"}
    headers = {"Content-Type": "application/json"}
    response = requests.request("GET", url, headers=headers, params=querystring).json() #response 객체를 json으로 반환
    try:
        with open(f"userdata/profile_{handle}.json", 'w') as userdata:
            json.dump(response, userdata, ensure_ascii=False, indent=4) #json 파일 쓰기
        return 1
    except:
        return 0

name = "uwoobeat"
res = get_info_from_solvedac(name)

with open(f"userdata/profile_{name}.json", 'w') as f:
    json.dump(res, f, ensure_ascii=False, indent=4)