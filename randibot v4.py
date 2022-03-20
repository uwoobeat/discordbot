import discord
import json
import requests
import os
from discord import Intents
from discord.ext import commands
from discord_slash import SlashCommand
import pymongo
from pymongo import MongoClient
import certifi

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


#solvedac 관련 함수

#사용자 정보를 json으로 가져오는 함수
def get_user_info(handle):
        url = "https://solved.ac/api/v3/user/show"
        querystring = {"handle":f"{handle}"}
        headers = {"Content-Type": "application/json"}
        return requests.request("GET", url, headers=headers, params=querystring).json() #return dict


#사용자 티어를 숫자에서 문자열로 변환하는 함수 
def convert_tier_num_to_str(tier_num): #tierdata는 깃허브에 저장해놓고 써도 될듯?
    f = open("C://discordbot/tierdata.txt")
    tierList = [f.readline().rstrip().split('\t') for _ in range(31)]
    return tierList[int(tier_num)-1][1]



#mongoDB 연결
with open('C://discordbot/connect_url.txt', 'r') as f:
    connect_url = f.readline().rstrip() #txt 파일에서 연결 위한 URL 불러오기
client_mongo = MongoClient(connect_url, tlsCAFile=certifi.where()) #클러스터 할당
#MongoDB는 보안 통신을 위해 TLS 인증서가 필요한데, python은 TLS 통해 요청 불가능하므로 대신 certifi 패키지를 통해 요청
db = client_mongo["randibot"] #randibot 데이터베이스 할당
entry_collection = db["entrydata"] #entrydata 컬렉션을 entry_collection으로 할당



#참가자 CRUD 기능

#참가자를 입력받는 명령어
@bot.command(aliases = ["신청"])
async def 참가(ctx, *handleList): #가변 매개변수로 한번에 여러 핸들명을 입력받기 
    success_handle_list = [] #신청 성공한 핸들
    failed_dup_handle_list = [] #중복으로 실패한 핸들
    failed_invalid_handle_list = [] #솔브닥에 정보 존재하지 않는 핸들

    for handle in handleList:
        if not entry_collection.find_one({"handle": f"{handle}"}): #만약 db에 핸들명이 존재하면
            try:
                tier = int(get_user_info(handle)["tier"]) #api 통해 티어 가져오기
                entry_collection.insert_one({"handle": f"{handle}", "tier": f"{tier}"}) #없으면 db에 핸들, 티어 저장
                success_handle_list.append(handle)
            except:
                failed_invalid_handle_list.append(handle) #solvedac api에서 오류 발생
        else:
            failed_dup_handle_list.append(handle)
    
    output = [
        f"등록에 성공한 핸들명 : {', '.join(success_handle_list)}",
        f"이미 존재하는 핸들명 : {', '.join(failed_dup_handle_list)}",
        f"유효하지 않은 핸들명 : {', '.join(failed_invalid_handle_list)}"
    ]

    await ctx.send('\n'.join(output))
    

#참가자 목록을 보여주는 명령어.
@bot.command(aliaes = ["신청현황"])
async def 신청목록(ctx):
    embed = discord.Embed(
        title = "신청자 현황",
        description = "현재까지 랜디를 신청한 멤버는 다음과 같습니다.",
        color = 0x6CCAD0
    )
    
    try: #티어에 따라 닉네임에 색 지정해주는 기능 추가 고려
        userdata = list(entry_collection.find())
        userdata.sort(key=lambda x: -int(x['tier']))

        for entryDict in userdata:
            embed.add_field(
                name = f"{entryDict['handle']}", 
                value = f"{convert_tier_num_to_str(entryDict['tier'])}", 
                inline = False
            ) 

        embed.set_footer(text = "Bot Made by uwoobeat & swoon")

        await ctx.send(embed = embed)

    except:
        await ctx.send("멤버 목록 로딩 중 오류가 발생했습니다.")


#참가자를 삭제하는 명령어
@bot.command(aliases =["삭제", "탈퇴"])
async def 제거(ctx, handle):
    if not (handle.isalnum() and len(handle) <= 20):
        await ctx.send("삭제하고자 하는 핸들명의 형식이 올바르지 않습니다. 알파벳과 숫자로 구성된 20자 이하의 핸들명을 입력해주세요.")
        return

    deleted_data = entry_collection.delete_one({"handle": f"{handle}"})

    if deleted_data:
        await ctx.send(f"{handle}님의 정보가 신청목록에서 성공적으로 제거되었습니다.")
    else:
        await ctx.send("등록되지 않은 멤버입니다.")


#신청된 참가자를 전부 삭제하는 명령어
@bot.command(aliases =["전체삭제"])
async def 전체제거(ctx):
    #사용자에게 정말로 제거할 것인지 묻고, 응답 받아서 처리해야 함
    if entry_collection.delete_many({}):
        await ctx.send("전체 신청정보가 성공적으로 제거되었습니다.")
    else:
        await ctx.send("신청목록이 비어있거나, 처리 중 에러가 발생하였습니다.")
    


#토큰 불러오기
f = open("C://discordbot/token.txt", 'r')
token = f.readline().rstrip()
f.close()



#봇 실행
bot.run(token)