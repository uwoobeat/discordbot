import discord
import json
import requests
import os
from discord import Intents
from discord.ext import commands
from discord_slash import SlashCommand

bot = commands.Bot(command_prefix = '!', intents = Intents.default())
#slash = SlashCommand(bot, sync_commands = True)

#구동 확인
@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name = "랜디봇 테스트"))
    print("=" * 30)
    print(f"{bot.user.name}으로 로그인")
    print(f"Bot ID : {bot.user.id}")
    print(f"성공적으로 연결되었음")
    print("="* 30)

#read username.json

# username.json

#write username.json
"""
with open('C://discordbot/username.json', 'w') as w:
    entryJson = json.dumps(w, entryDict)
"""
    

#참가자 DB 관리

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

""""
def convert_tier_num_to_str(tier_num): #숫자로 입력된 티어를 영/한 문자열로 변환
    with open(f"tierdata")
"""

@bot.command() #참가자를 입력받는 명령어
async def 참가(ctx, handle):

    if not os.path.isfile("C://discordbot/entrydata.json"):
        entryDict = dict() #존재하지 않는 파일이면 불러오지 않기
    else:
        with open(f'C://discordbot/entrydata.json', 'r', encoding='utf-8') as entry:
            entryDict = json.load(entry) #load method를 통해 entryDict로 열기
    
    if handle not in entryDict.keys(): #핸들명이 참가자 목록에 존재하는지 확인
        url = "https://solved.ac/api/v3/user/show"
        querystring = {"handle":f"{handle}"}
        headers = {"Content-Type": "application/json"}
        response = requests.request("GET", url, headers=headers, params=querystring).json() #response 객체를 json으로 반환
        
        print(f"{handle} 쓰기 시작")
        
        with open(f"C://discordbot/userdata/profile_{handle}.json", 'w', encoding='utf-8') as userdata:
        #### 현재 이 구간에서 문제 발생 중 ####
            json.dump(response, userdata, indent=4) #json 파일 쓰기
            userdata.close()
        
        print(f"{handle} 쓰기 종료")

        with open(f"C://discordbot/userdata/profile_{handle}.json", 'r', encoding='utf-8') as userdata:
            userProfile = json.load(userdata)

        userTier = userProfile["tier"]
        entryDict[handle] = dict()
        entryDict[handle]["tier"] = userTier

        await ctx.send(f"{entryDict}")

        #dump method를 통해 수정된 entryDict를 저장
        with open(f'C://discordbot/entrydata.json', 'w', encoding='utf-8') as entry:
            json.dump(entryDict, entry, indent=4)
        
        await ctx.send(f"{handle}님의 정보가 성공적으로 참가자 DB에 등록되었습니다.")

        #예외 발생 시 파일 close 후 메세지 출력
        await ctx.send("정보 등록 중 오류가 발생했습니다.")

    else:
        await ctx.send("이미 등록된 유저입니다.")
    #완료 후 파일 close


@bot.command() #참가자를 수정하는 명령어
async def 수정(ctx, handle_before, handle_after):
    with open(f'C://discordbot/entrydata.json', 'r', encoding='utf-8') as entry:
        entryDict = json.load(entry) #load method를 통해 entryDict로 열기
    nameList = entryDict.keys()

    if handle_before in nameList and handle_after not in nameList: 
    #수정할 핸들명이 참가자 목록에 존재하는지, 바꿀 핸들명이 목록에 존재하지 않는지 확인
        try:
            tmp = entryDict[handle_before] #tmp에 해당 핸들의 dict 정보 저장
            del entryDict[handle_before] #기존 핸들 정보 삭제
            entryDict[handle_after] = tmp #새 핸들에 해당 정보 할당

            #dump method를 통해 수정된 ntryDict를 저장
            with open(f'C://discordbot/entrydata.json', 'w', encoding='utf-8') as entry:
                json.dump(entryDict, entry, indent=4)
            await ctx.send(f"{handle_before}을 {handle_after}(으)로 성공적으로 수정하였습니다.")

        except:
            await ctx.send("정보 수정 중 오류가 발생했습니다.")
            entry.close()
    else:
        await ctx.send("등록되지 않은 유저이거나, 변경할 핸들명이 이미 등록된 상태입니다.")
    
    entry.close()


@bot.command() #참가자 목록을 보여주는 명령어
async def 신청목록(ctx):
    embed = discord.Embed(
        title = "신청자 현황",
        description = "현재까지 랜디를 신청한 멤버는 다음과 같습니다.",
        color = 0x6CCAD0
    )
    
    try:
        with open(f'C://discordbot/entrydata.json', 'r', encoding='utf-8') as entry:
            entryDict = json.load(entry) #load method를 통해 entryDict로 열기
        
        for handle in entryDict:
            embed.add_field(name = f"{handle}", value = f"tier: {entryDict[handle]['tier']}",inline = False)

        embed.set_footer(text = "Bot Made by uwoobeat & swoon")

        await ctx.send(embed = embed)

    except:
        await ctx.send("멤버 목록 로딩 중 오류가 발생했습니다.")
        entry.close()

"""
@bot.command() #참가자를 삭제하는 명령어
async def 삭제(ctx, handle):
"""

f = open("C://discordbot/token.txt", 'r')
token = f.readline().rstrip()
f.close()

bot.run(token)