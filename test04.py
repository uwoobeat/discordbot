def convert_tier_num_to_str(tier_num): #숫자로 입력된 티어를 영/한 문자열로 변환
    f = open("C://discordbot/tierdata.txt")
    tierList = [f.readline().rstrip().split('\t') for _ in range(31)]
    tier_str = tierList[tier_num-1][1]
    return tier_str
    

print(convert_tier_num_to_str(5))