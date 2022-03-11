import requests
import random

url = "https://solved.ac/api/v3/search/problem"

username_dict = open("username.txt") #dict지만 일단은 리스트 쓴다
print(username_dict)
#참가자 리스트. 나중에 json으로 변환해서 랜디 결과 확인 및 통계분석 용이하게...
tier_list = ["G3", "G4", "S1", "G5"] #참가자들의 티어. 나중에 username.json에서 빼올 것


query_min_tier = "S1" #참가자 최소 티어. 나중에 tier 객체로 표현
query_max_tier = "G5" #참가자 최대 티어
query_solved = 200 #최소 풀이 인원 제한. 나중에 command 인자로 받아와서 처리
query_solved_by = ' '.join(["solved_by:" + name for name in username_dict]) #solved by: (유저이름) 이은 문자열

querystring = {
    "query":f"tier:{query_min_tier}..{query_max_tier} {query_solved_by}",
    "sort":"random" #모든 페이지를 가져올 수 없으므로, 랜덤정렬하여 나온 첫 100개만 받음
    }

class queryOverflowError(Exception):
    print("쿼리 문자열은 500자를 넘을 수 없습니다.")
    print(f"쿼리 문자열 길이 = {len(querystring)}")
    print("=" * 30)
    print(querystring)
    print("=" * 30)

if len(querystring) > 500:
    raise queryOverflowError

headers = {"Content-Type": "application/json"}
response = requests.request("GET", url, headers=headers, params=querystring)

def makeProbleSet(pro_list, pro_num):
    """
    :param pro_list: 정렬된 문제 객체 리스트
    :param pro_num: 추천 문제 개수 
    :return selected_problems: 만들어진 문제셋
    """
    pro_list_size = len(pro_list)
    selected_problems = []
    step = (pro_list_size-1)//(pro_num-1)

    cnt = 0
    for i in range(0, pro_list_size-1, step):
        selected_problems.append(pro_list[i])
        cnt += 1
        if cnt == pro_num: break
    if len(selected_problems) != pro_num:
        print(len(selected_problems))
        raise #원하는 개수만큼 문제가 추천되지 않았을 때 (전체 표본이 적을 때 오류 발생 가능)
    else:
        return selected_problems


problem_list = sorted(response.json()["items"], key=lambda x:x["level"])

problemset = makeProbleSet(problem_list, 8)
for i in problemset: print(i["problemId"], i["level"])

#문제셋 추천 완료


"""
티어에 대해 작동하는 add, sub 함수 구현
>> 간단하게 n5, 1
"""

"""
실버3 ~ 골드3 했는데, 골드5가 없다...
균등한 난이도 분포를 보장해야 함
만약에 분포가 멸망했으면 재요청

분포가 잘 됐는지 판단하는 값(ex : 분포율)
재요청 제한을 걸어두자. 너무 오래 걸리지 않게...
"""





