# bot.py
import os
import math
import time
import discord
import random
import subprocess
from discord.ext import commands
TOKEN =  ''

AllMessages = []
bot = commands.Bot(intents=discord.Intents.all(),command_prefix = 'pi ')



class Datee:
    def __init__(self, years=0, days=0):
        self.years = years
        self.days = days

month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

def generate_random_date():
    ret = Datee()
    ret.years = random.randint(0, 1)
    ret.days = random.randint(1, 365)
    return ret

def generate_date_from_days(days):
    y = days // 365
    days = (days-1) % 365+1
    return Datee(years=y, days=days)

def convert_datee_to_format(date_):
    y = date_.years
    days = date_.days
    current_month = 1
    while days > 0:
        if month[current_month - 1] < days:
            days -= month[current_month - 1]
            current_month += 1
        else:
            break
    ret = ""
    if days < 10:
        ret += '0'
    ret += str(days)
    ret += '/'
    if current_month < 10:
        ret += '0'
    ret += str(current_month)
    ret += '/'
    ret += str(y + 2025)
    return ret

def get_date_difference_in_days(start_date, end_date):
    return (end_date.years * 365 + end_date.days) - (start_date.years * 365 + start_date.days)

def get_days(date_):
    return date_.years * 365 + date_.days

def advance_date_by_days(start_date, days):
    return generate_date_from_days(get_days(start_date) + days)

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
@bot.command(name="ping")
async def ping(ctx):
    await ctx.send('pong! {} ms'.format(round(bot.latency * 1000)))
@bot.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel_send(f'{member.name} hiiiiii')
def check(author):
    def inner_check(message):
        return message.author == author
    return inner_check
@bot.event
async def on_message(message: discord.Message):
    ctx = await bot.get_context(message)
    await bot.invoke(ctx)
@bot.command(name='test')
async def testt(ctx, official:int):
    msg_x = await bot.wait_for('message',check=check(ctx.author), timeout=60)
    await ctx.send(str(msg_x.content))
@bot.command(name='add')
async def add_puzzle(ctx, official:int):
    d1 = random.randint(-29,29)
    d2 = random.randint(1,12)*30
    d3 = random.randint(-2,5)
    d4 = random.randint(0,1)*365
   # if str(ctx.message.author) == "yahiaahmed":
   #     if d4<365:
   #         d4=365
   #     if random.randint(0,15) == 0:
   #         d4=0
   #     if abs(d1) < 10:
   #         d1=random.randint(20,31)
   #         if random.randint(0,1) == 0:
   #             d1*=-1
    answer = d2+d1+d3+d4

    await ctx.send(f"{ctx.author.mention}"+"\n" + str(d1) + "\n" + str(d2) + "\n" + str(d3) + "\n" + str(d4))
    start = time.time()
    msg_x = await bot.wait_for('message',check=check(ctx.author), timeout=60)
    x_guess = int(msg_x.content)
    end = time.time()
    #score = 3/(abs(answer-x_guess)+1)*(60-(end-start))*0.67
    d=abs(answer-x_guess)
    score = max(0,180-math.log((math.sqrt((end-start)+0.5)+d**1.3)**0.7)*100)
    await ctx.send(f"{ctx.message.author.mention}"+" \n" + "time = " + f"{end-start:.2f}" + "\n" + "diff = " + str(answer-x_guess)+ "\nscore = " + f"{score:.2f}")
    print("author in add: " + str(ctx.message.author))
    if official == 1:
        file_name = str(ctx.message.author) + "2.txt"
        with open(file_name, 'a') as file:
            file.write(str(score) + '\n')

@bot.command(name='puzzle', aliases = ['solve'])
async def give_puzzle(ctx,official:int):
    d1 = generate_random_date()
    d2 = generate_random_date()
    if get_days(d1) > get_days(d2):
        d1, d2 = d2, d1

    answer = get_date_difference_in_days(d1, d2)

    await ctx.send(f"{ctx.author.mention}"+"\nStart date:" + convert_datee_to_format(d1) + "\n" + "End date:" + convert_datee_to_format(d2))

    start = time.time()
    msg_x = await bot.wait_for('message',check=check(ctx.author), timeout=60)
    x_guess = int(msg_x.content)
    end = time.time()
    #score = 3/(abs(answer-x_guess)+1)*(60-(end-start))*0.67
    d=abs(answer-x_guess)
    score = max(0,180-math.log((math.sqrt((end-start)+0.5)+d**1.3)**0.7)*100)
    if str(ctx.message.author) == "yahiaahmed":

        if answer - x_guess != 0:
            await ctx.send("you should work on your method btw")
        if answer-x_guess == 365:
            await ctx.send("lmao someone forgot to check the year, dude work on the year")
        elif answer >= 365:
            await ctx.send("having trouble with adding 365?")
        elif answer < 65:
            if score>90:
                await ctx.send("you don't have trouble with small differences..")
            else:
                await ctx.send("Having trouble with small differneces??")
    await ctx.send(f"{ctx.message.author.mention}"+" \n" + "time = " + f"{end-start:.2f}" + "\n" + "diff = " + str(answer-x_guess)+ "\nscore = " + f"{score:.2f}")
    if official == 1:
        print("author in add: " + str(ctx.message.author))
        file_name = str(ctx.message.author) + ".txt"
        with open(file_name, 'a') as file:
            file.write(str(score) + '\n')

@bot.command(name='addh')
async def addh_puzzle(ctx, official:int):
    d1 = random.randint(-29,29)
    d2 = random.randint(1,12)
    d3 = random.randint(-2,5)
    d4 = random.randint(0,1)*365
    if str(ctx.message.author) == "yahiaahmed":
        if d4<365:
            d4=365
        if random.randint(0,15) == 0:
            d4=0
        if abs(d1) < 10:
            d1=random.randint(20,31)
            if random.randint(0,1) == 0:
                d1*=-1
    answer = d2*30+d1+d3+d4

    await ctx.send(f"{ctx.author.mention}"+"\n" + str(d1) + "\n" + str(d2) + "*30\n" + str(d3) + "\n" + str(d4))
    start = time.time()
    msg_x = await bot.wait_for('message',check=check(ctx.author), timeout=60)
    x_guess = int(msg_x.content)
    end = time.time()
    #score = 3/(abs(answer-x_guess)+1)*(60-(end-start))*0.67
    d=abs(answer-x_guess)
    score = max(0,180-math.log((math.sqrt((end-start)+0.5)+d**1.3)**0.7)*100)
    await ctx.send(f"{ctx.message.author.mention}"+" \n" + "time = " + f"{end-start:.2f}" + "\n" + "diff = " + str(answer-x_guess)+ "\nscore = " + f"{score:.2f}")
    if official == 1:
        file_name = str(ctx.message.author) + "3.txt"
        with open(file_name, 'a') as file:
            file.write(str(score) + '\n')
@bot.command(name = 'stats')
async def get_stats(ctx, user_id="?"):

    # Define the file name
    #await ctx.send(str(ctx.message.content))
    #print(str(ctx.message.content)[11:-2])
    #user = await bot.fetch_user(int(str(ctx.message.content)[11:-2]))
    #print(int(user_id[2:-2]))
    print(user_id)
    if user_id == "?":
        user = ctx.message.author
    else:
        user = await bot.fetch_user(int(user_id[2:-1]))
    #await ctx.send(str(user.name))
    file_name = str(user.name) + ".txt"
    my_list=[]
    with open(file_name, 'a') as file:
        print("new file created")
    with open(file_name, 'r') as file:
        for line in file:
            # Convert each line to an integer and append to the list
            my_list.append(float(line.strip()))
    sum5=0.0
    cnt5=0
    sum12=0.0
    cnt12=0
    for element in my_list[-5:]:
        sum5+=element
        cnt5+=1
    for element in my_list[-12:]:
        sum12+=element
        cnt12+=1
    bestao5sum=0.0
    bestao5=0.0
    bestao12=0
    bestao12sum=0.0
    personal_best=0
    for element in my_list:
        personal_best=max(personal_best, element)
    if len(my_list)>=5:
        for i in range(len(my_list)):
            bestao5sum+=my_list[i]
            if i>=4:
                bestao5 = max(bestao5, bestao5sum/5.00)
                bestao5sum-=my_list[i-4]

    if len(my_list)>=12:
        for i in range(len(my_list)):
            bestao12sum+=my_list[i]
            if i>=12:
                bestao12 = max(bestao12, bestao12sum/12.00)
                bestao12sum-=my_list[i-11]
    if cnt5 == 0:
        await ctx.send("no previous solves...")
    else:
        ao5 = sum5/cnt5
        ao12 = sum12/cnt12
        await ctx.send("```\nPersonal best: " + f"{personal_best:.2f}\n" + "Average of last 5: " + "{:.2f}".format(ao5) + "\n" + "Average of last 12: " + f"{ao12:.2f}" + "\nBest ao5: " + f"{bestao5:.2f}\n" + "Best ao12: " + f"{bestao12:.2f}\n" + "number of solves: " + str(len(my_list)) + "```\n")

@bot.command(name = 'astats')
async def get_stats_add(ctx, user_id="?"):

    # Define the file name
    #await ctx.send(str(ctx.message.content))
    #print(str(ctx.message.content)[11:-2])
    #user = await bot.fetch_user(int(str(ctx.message.content)[11:-2]))
    #print(int(user_id[2:-2]))
    print(user_id)
    if user_id == "?":
        user = ctx.message.author
    else:
        user = await bot.fetch_user(int(user_id[2:-1]))
    #await ctx.send(str(user.name))
   # print("user name in astats " + str(user.name))
    usernamee = str(user.name)
   # print("usernamee " + usernamee)
    if usernamee == "ApplePieSolver":
        usernamee+="#2629"
    file_name = usernamee + "2.txt"
    print(file_name)
    my_list=[]
    with open(file_name, 'a') as file:
        print("new file created")
    with open(file_name, 'r') as file:
        for line in file:
            # Convert each line to an integer and append to the list
            my_list.append(float(line.strip()))
    sum5=0.0
    cnt5=0
    sum12=0.0
    cnt12=0
    for element in my_list[-5:]:
        sum5+=element
        cnt5+=1
    for element in my_list[-12:]:
        sum12+=element
        cnt12+=1
    bestao5sum=0.0
    bestao5=0.0
    bestao12=0
    bestao12sum=0.0
    personal_best=0
    for element in my_list:
        personal_best=max(personal_best, element)
    if len(my_list)>=5:
        for i in range(len(my_list)):
            bestao5sum+=my_list[i]
            if i>=4:
                bestao5 = max(bestao5, bestao5sum/5.00)
                bestao5sum-=my_list[i-4]

    if len(my_list)>=12:
        for i in range(len(my_list)):
            bestao12sum+=my_list[i]
            if i>=11:
                bestao12 = max(bestao12, bestao12sum/12.00)
                bestao12sum-=my_list[i-11]
    if cnt5 == 0:
        await ctx.send("no previous solves...")
    else:
        ao5 = sum5/cnt5
        ao12 = sum12/cnt12
        await ctx.send("```\nPersonal best: " + f"{personal_best:.2f}\n" + "Average of last 5: " + "{:.2f}".format(ao5) + "\n" + "Average of last 12: " + f"{ao12:.2f}" + "\nBest ao5: " + f"{bestao5:.2f}\n" + "Best ao12: " + f"{bestao12:.2f}\n" + "number of solves: " + str(len(my_list)) + "```\n")
@bot.command(name = 'ahstats')
async def get_stats_addh(ctx, user_id="?"):

    # Define the file name
    #await ctx.send(str(ctx.message.content))
    #print(str(ctx.message.content)[11:-2])
    #user = await bot.fetch_user(int(str(ctx.message.content)[11:-2]))
    #print(int(user_id[2:-2]))
    print(user_id)
    if user_id == "?":
        user = ctx.message.author
    else:
        user = await bot.fetch_user(int(user_id[2:-1]))
    #await ctx.send(str(user.name))
    file_name = str(user.name) + "3.txt"
    my_list=[]
    with open(file_name, 'a') as file:
        print("new file created")
    with open(file_name, 'r') as file:
        for line in file:
            # Convert each line to an integer and append to the list
            my_list.append(float(line.strip()))
    sum5=0.0
    cnt5=0
    sum12=0.0
    cnt12=0
    for element in my_list[-5:]:
        sum5+=element
        cnt5+=1
    for element in my_list[-12:]:
        sum12+=element
        cnt12+=1
    bestao5sum=0.0
    bestao5=0.0
    bestao12=0
    bestao12sum=0.0
    personal_best=0
    for element in my_list:
        personal_best=max(personal_best, element)
    if len(my_list)>=5:
        for i in range(len(my_list)):
            bestao5sum+=my_list[i]
            if i>=4:
                bestao5 = max(bestao5, bestao5sum/5.00)
                bestao5sum-=my_list[i-4]

    if len(my_list)>=12:
        for i in range(len(my_list)):
            bestao12sum+=my_list[i]
            if i>=11:
                bestao12 = max(bestao12, bestao12sum/12.00)
                bestao12sum-=my_list[i-11]
    if cnt5 == 0:
        await ctx.send("no previous solves...")
    else:
        ao5 = sum5/cnt5
        ao12 = sum12/cnt12
        await ctx.send("```\nPersonal best: " + f"{personal_best:.2f}\n" + "Average of last 5: " + "{:.2f}".format(ao5) + "\n" + "Average of last 12: " + f"{ao12:.2f}" + "\nBest ao5: " + f"{bestao5:.2f}\n" + "Best ao12: " + f"{bestao12:.2f}\n" + "number of solves: " + str(len(my_list)) + "```\n")

@bot.command(name = 'lb')
async def leaderboard(ctx):
    # Define the file name
    file_name = "leaderboard.txt"
    name_list=[]
    with open(file_name, 'r') as file:
        for line in file:
            # Convert each line to an integer and append to the list
            name_list.append(str(line.strip()))
    name_list = list(set(name_list))
    scores = []
    for cur_name in name_list:
        my_list = []
        with open(str(cur_name)+".txt",'r') as file:
            for line in file:
                my_list.append(float(line.strip()))
        sum5 = 0.0
        cnt5 = 0
        sum12 = 0.0
        cnt12 = 0
        for element in my_list[-5:]:
            sum5 += element
            cnt5 += 1
        for element in my_list[-12:]:
            sum12 += element
            cnt12 += 1
        bestao5sum = 0.0
        bestao5 = 0.0
        bestao12 = 0
        bestao12sum = 0.0
        personal_best = 0
        for element in my_list:
            personal_best = max(personal_best, element)
        if len(my_list) >= 5:
            for i in range(len(my_list)):
                bestao5sum += my_list[i]
                if i >= 4:
                    bestao5 = max(bestao5, bestao5sum / 5.00)
                    bestao5sum -= my_list[i - 4]

        if len(my_list) >= 12:
            for i in range(len(my_list)):
                bestao12sum += my_list[i]
                if i >= 11:
                    bestao12 = max(bestao12, bestao12sum / 12.00)
                    bestao12sum -= my_list[i - 11]
        if cnt5 == 0:
            print("no solves")
        else:
            scores.append((cur_name, bestao5))

    scores.sort(key = lambda x:x[1],reverse = True)
    leaderbrd = ""
    for pairr in scores:
        leaderbrd += f"{pairr[0].ljust(20)}{f'{pairr[1]:.2f}'.rjust(6)}"
        leaderbrd += "\n"
    await ctx.send("```\n" + "\n"+leaderbrd+"```\n")


@bot.command(name = 'alb')
async def aleaderboard(ctx):
    # Define the file name
    file_name = "aleaderboard.txt"
    name_list=[]
    with open(file_name, 'r') as file:
        for line in file:
            # Convert each line to an integer and append to the list
            name_list.append(str(line.strip()))
    name_list = list(set(name_list))
    scores = []
    for cur_name in name_list:
        my_list = []
        with open(str(cur_name)+".txt",'r') as file:
            for line in file:
                my_list.append(float(line.strip()))
        sum5 = 0.0
        cnt5 = 0
        sum12 = 0.0
        cnt12 = 0
        for element in my_list[-5:]:
            sum5 += element
            cnt5 += 1
        for element in my_list[-12:]:
            sum12 += element
            cnt12 += 1
        bestao5sum = 0.0
        bestao5 = 0.0
        bestao12 = 0
        bestao12sum = 0.0
        personal_best = 0
        for element in my_list:
            personal_best = max(personal_best, element)
        if len(my_list) >= 5:
            for i in range(len(my_list)):
                bestao5sum += my_list[i]
                if i >= 4:
                    bestao5 = max(bestao5, bestao5sum / 5.00)
                    bestao5sum -= my_list[i - 4]

        if len(my_list) >= 12:
            for i in range(len(my_list)):
                bestao12sum += my_list[i]
                if i >= 11:
                    bestao12 = max(bestao12, bestao12sum / 12.00)
                    bestao12sum -= my_list[i - 11]
        if cnt5 == 0:
            print("no solves")
        else:
            scores.append((cur_name, bestao5))

    scores.sort(key = lambda x:x[1],reverse = True)
    leaderbrd = ""
    for pairr in scores:
        leaderbrd += f"{pairr[0].ljust(20)}{f'{pairr[1]:.2f}'.rjust(6)}"
        leaderbrd += "\n"
    await ctx.send("```\n" + leaderbrd+"```\n")


@bot.command(name = 'ahlb')
async def ahleaderboard(ctx):
    # Define the file name
    file_name = "ahleaderboard.txt"
    name_list=[]
    with open(file_name, 'r') as file:
        for line in file:
            # Convert each line to an integer and append to the list
            name_list.append(str(line.strip()))
    name_list = list(set(name_list))
    scores = []
    for cur_name in name_list:
        my_list = []
        with open(str(cur_name)+".txt",'r') as file:
            for line in file:
                my_list.append(float(line.strip()))
        sum5 = 0.0
        cnt5 = 0
        sum12 = 0.0
        cnt12 = 0
        for element in my_list[-5:]:
            sum5 += element
            cnt5 += 1
        for element in my_list[-12:]:
            sum12 += element
            cnt12 += 1
        bestao5sum = 0.0
        bestao5 = 0.0
        bestao12 = 0
        bestao12sum = 0.0
        personal_best = 0
        for element in my_list:
            personal_best = max(personal_best, element)
        if len(my_list) >= 5:
            for i in range(len(my_list)):
                bestao5sum += my_list[i]
                if i >= 4:
                    bestao5 = max(bestao5, bestao5sum / 5.00)
                    bestao5sum -= my_list[i - 4]

        if len(my_list) >= 12:
            for i in range(len(my_list)):
                bestao12sum += my_list[i]
                if i >= 11:
                    bestao12 = max(bestao12, bestao12sum / 12.00)
                    bestao12sum -= my_list[i - 11]
        if cnt5 == 0:
            print("no solves")
        else:
            scores.append((cur_name, bestao5))

    scores.sort(key = lambda x:x[1],reverse = True)
    leaderbrd = ""
    for pairr in scores:
        leaderbrd += f"{pairr[0].ljust(20)}{f'{pairr[1]:.2f}'.rjust(6)}"
        leaderbrd += "\n"
    await ctx.send("```\n" + "\n"+leaderbrd+"```\n")




bot.run(TOKEN)


