import json
import requests
import pymongo
import certifi
from pymongo import MongoClient

with open('C://discordbot/connect_url.txt', 'r') as f:
    connect_url = f.readline().rstrip() #txt 파일에서 연결 위한 URL 불러오기

print(connect_url)


#client_mongo = MongoClient(connect_url, tlsCAFile=certifi.where()) #클러스터 할당
#MongoDB는 보안 통신을 위해 TLS 인증서가 필요한데, python은 TLS 통해 요청 불가능하므로 대신 certifi 패키지를 통해 요청


client_mongo = pymongo.MongoClient(connect_url)
db = client_mongo["randibot"]
entry_collection = db["entrydata"] #userdata db의 entrydata 컬렉션을 entry_collection으로 할당


handleList = ["uwoobeat", "swooon"]

userdata = [
                {
                    "handle": "uwoobeat",
                    "tier": 16
                },
                {
                    "handle": "swoon",
                    "tier": 25
                }
            ]   


def get_userdata(handle):
        url = "https://solved.ac/api/v3/user/show"
        querystring = {"handle":f"{handle}"}
        headers = {"Content-Type": "application/json"}
        return requests.request("GET", url, headers=headers, params=querystring).json() #return dict

entry_collection.insert_many(userdata)

print(entry_collection.count_documents({"handle":"uwoobeat"}))

for handle in handleList:
    if not entry_collection.count_documents({"handle":f"{handle}"}):
        tier = get_userdata(handle)["tier"]
        entry_collection.insert_one({"handle": f"{handle}", "tier": f"{tier}"})
    
