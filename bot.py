from sre_constants import JUMP
from urllib.parse import urljoin
import discord
from discord import Intents
from discord.ext import commands
from discord_slash import SlashCommand
from discord_slash.utils.manage_commands import create_option, create_choice

bot = commands.Bot(command_prefix = '!', intents = Intents.default())
slash = SlashCommand(bot, sync_commands = True)
nameDict = {}


@bot.event
async def on_ready():
    await bot.change_presence(activity = discord.Game(name = "코노봇 테스트"))
    print("=" * 30)
    print(f"{bot.user.name}으로 로그인됨")
    print(f"Bot ID : {bot.user.id}")
    print(f"성공적으로 연결됨")
    print('=' * 30)


@bot.command()
async def embed(ctx):
    embed = discord.Embed(title = "제목입니다.", description = "설명입니다.", color = 0x6CCAD0)
    embed.set_thumbnail(url='https://i.imgur.com/CsEK6bs.gif')
    for i in range(1,4):
        embed.add_field(name = f"소제목{i}", value = f"{i}번째 내용입니다.", inline = False)
    embed.set_footer(
        text = "Bot Made by 유우비트",
        icon_url = "https://www.inven.co.kr/common/image/viewer.php?loc=&file=https%3A%2F%2Fupload3.inven.co.kr%2Fupload%2F2021%2F06%2F22%2Fbbs%2Fi14216404895.jpg")
    
    await ctx.send(embed = embed)


@bot.command(aliases = ['안녕하세요', 'Hello', 'hi', '안녕']) #Hello 등 명령어를 받으면 응답
async def hello(ctx):
    await ctx.send(f"{ctx.author.mention}님도 안녕!")


@bot.command(aliases = ['repeat']) #echo 등 명령어를 받으면 해당 메세지를 복사
async def echo(ctx, *, msg):
    await ctx.send(msg)


#멤버 등록

@bot.command(aliases = ['등록']) #create
async def 가입(ctx, name):
    try:
        if name not in nameDict:
            nameDict[name] = list()
            await ctx.send(f"{name}님의 정보가 성공적으로 등록되었습니다.")
        else:
            await ctx.send("이미 리스트에 존재하는 유저입니다.")
    except:
        await ctx.send("처리 중 에러 발생")


@bot.command(aliases = ['제거']) #delete
async def 탈퇴(ctx, name):
    try:
        nameDict.pop(name)
        await ctx.send(f"{name}님의 정보가 성공적으로 제거되었습니다.")
    except ValueError:
        await ctx.send("등록되지 않은 정보입니다.")
    except:
        await ctx.send("처리 중 에러 발생")


@bot.command() #read
async def 유저목록(ctx):
    embed = discord.Embed(
        title = "유저 목록", 
        description = "현재 존재하는 멤버 리스트는 다음과 같습니다.", 
        color = 0x6CCAD0)
    embed.set_thumbnail(url='https://i.imgur.com/CsEK6bs.gif')
    for name in nameDict.keys():
        embed.add_field(name = f"{name}", value = f"{name}에 대한 정보", inline = False)
    embed.set_footer(text = "Bot Made by 유우비트")
    
    await ctx.send(embed = embed)


@bot.command() #update
async def 수정(ctx, name_before, name_after):
    try:
        if name_before in nameDict.keys():
            tmpValue = nameDict[name_before]
            nameDict.pop(name_before)
            nameDict[name_after] = tmpValue
            await ctx.send(f"{name_before}님의 이름이 {name_after}(으)로 변경되었습니다.")
        else:
            raise Exception
    except:
        await ctx.send("존재하지 않는 이름이거나 변경 중 에러가 발생했습니다.")


@slash.slash(
    name = "백준",
    description = "백준 온라인 저지로 이동합니다.",
    options = [
        create_option(
            name = "카테고리",
            description = "원하는 카테고리를 입력해주세요.",
            option_type = 3, #입력받는 값의 데이터 형식
            required = True,
            choices = [
                create_choice(
                    name = "문제",
                    value = "문제"
                ),
                create_choice(
                    name = "문제집",
                    value = "문제집"
                ),
                create_choice(
                    name = "대회", 
                    value = "대회"
                ),
                create_choice(
                    name = "랭킹",
                    value = "랭킹"
                ),
                create_choice(
                    name = "게시판",
                    value = "게시판"
                )
            ] #imported from create_choice
        )
    ],
    connector = {'카테고리':'boj_category'},
    #option name와 함수 param은 일치해야 한다. 이 경우 한글 옵션네임을 사용할 수 없다.
    #따라서 slash에서 제공하는 connector 인자를 통해 옵션이름과 인자이름를 연결시켜준다. 
    guild_ids = [824993450008117287]
)
async def command_boj(ctx, boj_category = "문제"):
    await ctx.send(f"Baekjoon Online judge에 오신 것을 환영합니다.\n{boj_category}(으)로 이동합니다.")


@slash.slash(
    name = "솔브닥",
    description = "solved.ac로 이동합니다.",
    options = [
        create_option(
            name = "카테고리",
            description = "원하는 카테고리를 입력해주세요.",
            option_type = 3,
            required = True,
            choices = [
                create_choice(
                    name = "문제",
                    value = "문제"
                ),
                create_choice(
                    name = "기여",
                    value = "기여"
                ),
                create_choice(
                    name = "랭킹", 
                    value = "랭킹"
                ),
                create_choice(
                    name = "정보",
                    value = "정보"
                )
            ] #imported from create_choice
        )
    ],
    connector = {'카테고리':'solvedac_category'},
    guild_ids = [824993450008117287]
)
async def command_solvedac(ctx, solvedac_category = "문제"):
    await ctx.send(f"solved.ac에 오신 것을 환영합니다.\n{solvedac_category}(으)로 이동합니다.")

    if solvedac_category == "문제":
        solvedac_embed = discord.Embed(
            title = "링크 열기", 
            url = "https://solved.ac/problems/level", 
            description = "solved.ac로 이동하기")
        await ctx.send(embed = solvedac_embed)
    
    elif solvedac_category == "기여":
        solvedac_embed = discord.Embed(
            title = "링크 열기", 
            url = "https://solved.ac/guideline", 
            description = "solved.ac로 이동하기")
        await ctx.send(embed = solvedac_embed)

    elif solvedac_category == "랭킹":
        solvedac_embed = discord.Embed(
            title = "링크 열기", 
            url = "https://solved.ac/guideline", 
            description = "solved.ac로 이동하기")
        await ctx.send(embed = solvedac_embed)

    elif solvedac_category == "정보":
        solvedac_embed = discord.Embed(
            title = "링크 열기", 
            url = "https://solved.ac/rules", 
            description = "solved.ac로 이동하기")
        await ctx.send(embed = solvedac_embed)


bot.run('OTI0MDAwNjEyMTQyNjk0NDQx.YcYMoQ.4AbEzV9jeztNFkKnZo2zdfCW9co')