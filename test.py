#run.py
import discord

client = discord.Client()

@client.event
async def on_ready():
    print(f"We have logged in as {client}") #봇이 실행되면 콘솔창에 표시

@client.event
async def on_message(message):
    if message.author == client.user: # 봇 자신이 보내는 메세지는 무시
        return

    if message.content.startswith(";hello"): # 만약 $hello로 시작하는 채팅이 올라오면
        await message.channel.send("스운님 안녕하세요") # ~라고 보내기

client.run('OTI0MDAwNjEyMTQyNjk0NDQx.YcYMoQ.4AbEzV9jeztNFkKnZo2zdfCW9co') #토큰