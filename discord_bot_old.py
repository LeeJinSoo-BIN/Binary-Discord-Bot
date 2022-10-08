import discord, asyncio
#from discord.ext import commands
#from discord.ext import tasks


import requests
from bs4 import BeautifulSoup
from datetime import datetime
import json
import os


#bot = commands.Bot(command_prefix='!')

client = discord.Client()
token = "OTU0Mzc3Nzc4OTg2MzczMTYw.GXGlTG.lmblfqsEWlhPkWsb9iocFWlrpKlr7tFCbzsNeY"
#channel_id = 963024233414397962 #현황 채널
channel_id = 957992975328219146 #디버깅 채널

guild_id = 909357916677623869
code_block = False
crawl_with_group = True

@client.event
async def on_ready(): # 봇이 실행 준비가 되었을 때 행동할 것
    print('Logged in as')
    print(client.user.name) # 클라이언트의 유저 이름을 출력합니다.
    print(client.user.id) # 클라이언트의 유저 고유 ID를 출력합니다.
    # 고유 ID는 모든 유저 및 봇이 가지고있는 숫자만으로 이루어진 ID입니다.
    task = asyncio.create_task(alarm_every_Oclock())
    await task
    print('------')

'''
@bot.command(aliases=['안녕','hi','ㅎㅇ','ㅎ2'])
async def hello(ctx):
    await ctx.send("안녕하세요!")

'''



@client.event
async def on_message(msg):
    """
    Function to handle message dispatch
    For commands we check if certain ones are equal length to desired commands
    """
    if msg.author == client.user: # 만약 메시지를 보낸 사람과 봇이 서로 같을 때
        return
    #auth = str(msg.author.id)
    m = msg.content.strip()
    m = m.split(" ")
    print(m)
    print(msg)
    print(msg.content)
    if "!잔디" == m[0] :
        if len(m) == 1 :
            await send_message(channel_id, "!잔디 시작일 20220328\n!잔디 그룹 13898\n!잔디 추가 binary01 18011821이진수\n!잔디 제외 binary01\n!잔디 현황")

        elif "시작일" == m[1]:
            if (len(m) == 3) and (m[2].isnumeric()) and (len(m[2])==8):
                write_start_day(int(m[2]))
                await send_message(channel_id, "저장 완료")
            else :
                await send_message(channel_id, "입력 오류 (ex !잔디 시작일 20220328)")

        elif "그룹" == m[1]:
            if (len(m) == 3) and (m[2].isnumeric()) and (len(m[2])==5):
                write_group_id(m[2])
                await send_message(channel_id, "저장 완료")
            else :
                await send_message(channel_id, "입력 오류 (ex !잔디 그룹 13898)")
        
        elif "추가" == m[1]:
            if (len(m)==4 or len(m)==5) :                
                if len(m) == 5 :
                    name = m[3] +" "+m[4]
                else :
                    name = m[3][:8] +" " + m[3][8:]
                write_nickNname(m[2], name)
                await send_message(channel_id, "저장 완료")
            else :
                await send_message(channel_id, "입력 오류 (ex !잔디 추가 binary01 18011821이진수)")
        
        elif "제외" == m[1]:
            if len(m) == 3:
                #write_ignore_list(m[2])
                if del_nick(m[2]) :
                    await send_message(channel_id, "저장 완료")
                else :
                    await send_message(channel_id, "목록에 없는 닉네임 입니다.")
            else :
                await send_message(channel_id, "입력 오류 (ex !잔디 제외 binary01)")

        elif "현황" == m[1]:
            if len(m) == 2:
                await print_memeber_status()
            else :
                await send_message(channel_id, "입력 오류 (ex !잔디 현황)")
        
        # elif "추가" == m[1]:
        #     if len(m) == 3 :
        #         if (del_ignore_list(m[2])):
        #             await send_message(channel_id, "제외 목록에 없습니다.")
        #         else :
        #             await send_message(channel_id, "저장 완료")
                
        #     else :
        #         await send_message(channel_id, "입력 오류 (ex !잔디 추가 binary01)")
        
        else :
            await send_message(channel_id, "입력 오류 \n!잔디 시작일 20220328\n!잔디 그룹 13898\n!잔디 추가 binary01 18011821이진수\n!잔디 제외 binary01\n!잔디 현황")
        
                


            


async def send_message(channel_id, msg):
    channel = client.get_channel(channel_id)
    return await channel.send(msg)






def crawl(url, cookies={}, headers={"User-Agent": "Mozilla/5.0"}, save_html=False, filepath = "tmp.html", open_page=False):

    html = requests.get(url, cookies = cookies, headers=headers)    
    soup = BeautifulSoup(html.text, 'html.parser')
    if open_page == True :
        save_html = True

    if save_html:
        
        with open(filepath, 'w', encoding ="utf-8") as f:        
            f.write(html.text)
            f.close()
        if open_page:
            import webbrowser    
            webbrowser.open_new_tab(filepath)
    return soup

def get_members(group_id):
    members = []    
    url = "https://www.acmicpc.net/group/ranklist/"+group_id
    soup = crawl(url)
    
    div_admin_member = soup.select_one("div#admin_member")
    div_team_member = soup.select_one("div#team_member")

    for mem in div_admin_member.find_all("h4") :
        members.append(mem.text.split(" ")[0][1:])

    for mem in div_team_member.find_all("h4") :    
        members.append(mem.text.split(" ")[0][1:].split("\n")[0])

    return members

def plant_grass(start_day, today, seed) :

    field = ""
    total_grass_num = 0
    grass_num = 0
    total_day = 0
    counting_day = start_day
    max = 0
    while (counting_day != today+1):
        
        year = counting_day//10000
        month = counting_day//100%100
        day = counting_day%100
        
        if (day == 32 ) and (month in [1,3,5,7,8,10, 12]):            
            if month == 12:
                year += 1
                month = 1
                day = 1
            else :
                month += 1
                day = 1            
        elif (day == 31) and (month in [4,6,9,11]) :        
                month +=1
                day = 1
        elif ((day == 29) and (month == 2)) :
            if not((year % 4 == 0 and year % 100 != 0) or year % 400 == 0):
                month += 1
                day = 1
        elif (day == 30) and (month == 2):
            if ((year % 4 == 0 and year % 100 != 0) or year % 400 == 0):
                month += 1
                day = 1        
        counting_day = int(("%04d%02d%02d")%(year,month,day))

        if str(counting_day) in seed :            
            if code_block:
                field += "[32m■[0m"
            field += "■"
            grass_num += 1
            total_grass_num += 1
        else :            
            if code_block:
                field += "[33m□[0m"
            field += "□"
            if grass_num > 0:
                if max < grass_num :
                    max = grass_num
                grass_num = 0

        

        day += 1
        total_day += 1
        counting_day = int(("%04d%02d%02d")%(year,month,day))

    field+= "   ( "+str(total_grass_num)+" / " +str(total_day)+" )"
    if grass_num > 0:
        if max < grass_num :
            max = grass_num
        grass_num = 0
    if max > 0 :
        field+="\n최대 "+str(max)+"일 연속!!"
    field+="\n\n"    
    return field
    
def get_day_problems(members, start_day, members_name, ignore_list):

    today = int(datetime.today().strftime('%Y%m%d'))
    text=""

    for mem in members :

        if mem in ignore_list :
            continue

        url = "https://www.acmicpc.net/user/" + mem
        soup = crawl(url)
        scripts = soup.find_all("script") 


        for script in scripts :
            if "user_day_problems" in script.text :                
                user_day_problems = script.text
                break   
        if mem in members_name.keys():
            text+=members_name[mem]
        else : text+=mem

        text +="\n"
        field = plant_grass(start_day, today, user_day_problems)
        text+=field

    return text


def save_new_data():
    data = {}
    data["start_day"] = 0
    data["ignore_list"] = []
    data["name"] = {}
    data["group_id"] = ""
    with open("data.json", "w", encoding='utf-8') as json_file:
        json.dump(data, json_file)  

def save_data(data):
    with open("data.json", "w", encoding='utf-8') as json_file:
        json.dump(data, json_file, indent="\t", ensure_ascii=False)  

def load_data():
    if (not("data.json" in os.listdir())):
        save_new_data()
    with open('data.json', encoding='UTF8') as f:
        data = json.load(f)
    return data

def write_ignore_list(name):
    data = load_data()
    data["ignore_list"].append(name)
    save_data(data)

def del_ignore_list(name):
    data = load_data()
    if name in data["ignore_list"] :
        data["ignore_list"].remove(name)
        save_data(data)
        return False
    else : 
        return True

def write_nickNname(nick,name):
    data = load_data()
    data["name"][nick] = name
    save_data(data)

def del_nick(nick):
    data = load_data()
    if nick in data["name"].keys():
        del data["name"]
        return True
    else:
        return False
    save_data(data)

def write_start_day(day):
    data = load_data()
    data["start_day"] = day
    save_data(data)


def write_group_id(id):
    data = load_data()
    data["group_id"] = id
    save_data(data)


def slice_ymd(ymd):
    year = ymd//10000
    month = ymd//100%100
    day = ymd%100
    return str(year)+"년 "+str(month)+"월 " +str(day)+"일\n"

async def load_saved_data():
    ok = 0
    data = load_data()
    start_day = data["start_day"]
    if start_day == 0:
        await send_message(channel_id, "시작일이 입력되어 있지 않습니다. \n(ex !잔디 시작일 20220328)")
        ok = 1
    group_id = data["group_id"]
    if group_id =="":
        await send_message(channel_id, "그룹 id가 입력되어 있지 않습니다. \n(ex !잔디 그룹 13898)")
        ok = 1
    members_name = data["name"]
    ignore_list = data["ignore_list"]
    return start_day, group_id, members_name, ignore_list, ok

async def print_memeber_status():

    print("start printing plant status")    
    start_day, group_id, members_name, ignore_list, ok = await load_saved_data()
    
    if ok == 1:
        print("데이터 부족")
        return
    today = int(datetime.today().strftime('%Y%m%d'))
    text = ""
    if code_block:    
        text += "```ansi\n"
        text += "[1m시작 일 : [0m"
        text += slice_ymd(start_day)
        text += "[1m기준 일 : [0m"
        text += slice_ymd(today)
        text += "\n"
    else :
        text += "시작 일 : "
        text += slice_ymd(start_day)
        text += "기준 일 : "
        text += slice_ymd(today)
        text += "\n"
    print("get members...")
    if crawl_with_group :
        members = get_members(group_id)    
    else :
        members = members_name.keys()

    print("get problems...")
    text += get_day_problems(members, start_day, members_name, ignore_list)
    print("printing status...")
    if code_block:    
        text +="```"
    await send_message(channel_id, text)    
    print("done!!!")

    


async def alarm_every_Oclock():
    err = 0
    while (True):
        
        if err == 0 and datetime.now().second == 0 :
            err = 1            
            #await print_memeber_status()
        else :
            err = 0
            
        
        await asyncio.sleep(1)
    return 0


client.run(token)
import atexit
atexit.register(client.stop())


#bot.run(token)













