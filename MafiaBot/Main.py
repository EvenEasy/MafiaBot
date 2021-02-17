import config
import time
import discord
from discord.ext import commands
from discord.utils import get
import random

client = commands.Bot(command_prefix='$')

@client.event
async def on_ready():
    File = open("Players", "r+")
    File.truncate(0)
    File.close()
    ListRoles = open("RolesMafia", "r+")
    ListRoles.truncate(0)
    ListRoles.close()
    File = open("Players", "r")
    Players = []
    for line in File:
        Players.append(line)
    if len(Players) > 4:
        config.Game_is_Started = 1
        config.UnJoin = 0
    elif len(Players) < 4:
        config.Game_is_Started = 0
        config.UnJoin = 0
    config.Diference = 0

    print('Bot is Connected!')

@client.event
async def on_member_joid(memder):
    channel = client.get_channel(779697732746739712)
    await channel.send(member.mention + " :grey_exclamation: **Welcome**")

@client.command(aliases = ['set_up', 'commands'])
async def set_up(ctx):
    await ctx.author.send(f'**Привет)))**\nЯ Emma, и я Мафия БОТ:3\nвот Список Комманд')
    emd = discord.Embed(title='Commands:')

    emd.add_field(name = '{}join'.format('$'), value='Присоединиться к Игре')
    emd.add_field(name = '{}start'.format('$'), value='Начать Игру')
    emd.add_field(name = '{}card'.format('$'), value='Забрать свою Карточку')
    emd.add_field(name = '{}mafia [name.mention]'.format('$'), value='Отпределиться кто Мафия')
    emd.add_field(name = '{}yes'.format('$'), value='Подтвердить!')
    emd.add_field(name = '{}go'.format('$'), value='Еслы уже все взяли карточку!')
    emd.add_field(name = '{}kill [index_player]'.format('$'), value='Убить, но если указать большое число чем можно, то никого не Убит')
    emd.add_field(name = '{}clear [how_many]'.format('$'), value='Очистка чата')

    await ctx.author.send(embed = emd)

@client.command()
async def clear(ctx, amount = 100):
    await ctx.channel.purge(limit = amount)
    await ctx.send("Было очищано: **{}**сообщений".format(amount))
    T = 5
    while T:
        mins, secs = divmod(T, 60)
        timer = '{:02d}:{:02d}'.format(mins, secs) 
        print(timer, end="\r") 
        time.sleep(1)
        T -= 1
    await ctx.channel.purge(limit = 1)


@client.command()
async def join(ctx):#registers at game
    if config.UnJoin == 0:
        channel_game = client.get_channel(787344727430397952)
        File = open("Players", "r")
        Players = []
        for Line in File:
            Players.append(Line)
        File.close()
        if len(Players) > 4:
            config.peopleIsReady = 1
        if str(ctx.author.mention) + "\n" in Players:
            await ctx.send(f'Вы уже есть в списке Игроков, ожидайте игру на канале {channel_game.mention}\nв Голосовом канале - https://discord.gg/C6Ur68Wnws')
        elif str(ctx.author.mention) + "\n" not in Players:
            File = open("Players", "a")
            File.write(str(ctx.author.mention) + "\n")
            File.close()
            role = get(ctx.author.guild.roles, name="Player🃏")
            await ctx.author.add_roles(role)
            print(f'[User: {ctx.author}] in game!')
            await ctx.send(f'Я вас добавила в Список играков, ожидайте начало игры на канале {channel_game.mention}\nИ тут - https://discord.gg/C6Ur68Wnws')
    else:
        await ctx.send(f'{ctx.author.mention} Игра уже началась,\nОжидайте следуещей игры!\n:3')

@client.command()
async def start(ctx):#game start
    if config.Game_is_Started == 0 or config.peopleIsReady == 1:
        config.Game_is_Started = 1
        channel_game = client.get_channel(787344727430397952)
        config.And_w_start = 1
        config.UnJoin = 1
        await channel_game.send(f'Ничинаем!')
        await channel_game.send(f'Чтобы забрать свою карточку, напишите команду ```$card```')
        File = open("Players", "r")
        File_Roles = open("RolesMafia", "r+")
        File_Roles.truncate(0)
        File_Roles.close()
        File_Roles = open("RolesMafia", "w")
        Players = []
        for Line in File:
            Players.append(Line)
        killer = random.randint(0, len(Players) + 1)
        config.MafiaIndex = killer
        for user in range(0, len(Players)):
            if user == killer:
                File_Roles.write("Mafia" + "\n")
            else:
                File_Roles.write("people" + "\n")
        File_Roles.close()
        await ctx.send(f'Ок, я Стартую игру\nИгра на {channel_game.mention}!')        
    else:
        await ctx.send('Ожидайте остольных игроков, Пожалуйста:3')

@client.command()
async def card(ctx):#get a card
    if config.Game_is_Started == 1:
        File = open("Players", "r")
        Roles_File = open("RolesMafia", "r")
        Players = []
        Roles = []
        for Line in File:
            Players.append(Line)
        for Lines in Roles_File:
            Roles.append(Lines)
        File.close()
        Roles_File.close()
        Index_player = Players.index(str(ctx.author.mention) + "\n")
        print(Index_player)
        if Roles[Index_player] == 'Mafia' + '\n':
            File = open("Mafia", "a")
            File.write(str(ctx.author.mention) + "\n")
            File.close()
            await ctx.author.send('Вы: **{}**'.format(Roles[Index_player]))
            await ctx.author.send('Чтобы выбрать жертву, напишите ```$kill [Number player]```\nвот список играков:')
            index = 0
            for Player in Players:
                await ctx.author.send('Number: {0}\nPlayer: {1}\n'.format(index + 1, Player))
                index += 1

        else:
            await ctx.author.send('Вы: **{}**'.format(Roles[Index_player]))
    else:
        await ctx.send('Игра ищё не началась!')

@client.command()
async def go(ctx):
    await ctx.channel.send(f'Начимаем **!**')
    Timers = 15
    while Timers:
        mins, secs = divmod(Timers, 60)
        timer = '{:02d}:{:02d}'.format(mins, secs) 
        print(timer, end="\r")
        time.sleep(1)
        Timers -= 1
    await ctx.send('Night\nГород засыпает!')
    
    T = 10
    while T:
        mins, secs = divmod(T, 60)
        timer = '{:02d}:{:02d}'.format(mins, secs) 
        print(timer, end="\r") 
        time.sleep(1)
        T -= 1
    await ctx.send("Просипаеться Мафия")
    T = 10
    while T:
        mins, secs = divmod(T, 60)
        timer = '{:02d}:{:02d}'.format(mins, secs) 
        print(timer, end="\r") 
        time.sleep(1)
        T -= 1
    await ctx.send(f'Мафия виберает жертву через Команду ```$Kill [Number Player]```')

@client.command()
async def kill(ctx, i = 1):
    File = open("Players", "r")
    Players = []
    for Line in File:
        Players.append(Line)
    File.close()
    FileMafia = open("Mafia", "r")
    Mafias = []
    for Line in FileMafia:
        Mafias.append(Line)
    if str(ctx.author.mention) in Mafias:
        try:
            File = open("Players", "r")
            Players = []
            for line in File:
                Players.append(line)
            Killed = Players[i - 1]
            T = 5
            while T:
                mins, secs = divmod(T, 60)
                timer = '{:02d}:{:02d}'.format(mins, secs) 
                print(timer, end="\r")
                time.sleep(1)
                T -= 1
            channel = client.get_channel(787344727430397952)
            await channel.send('Игрок: {}\nБыл Убит Мафией'.format(Killed.mention))
            T = 5
            while T:
                mins, secs = divmod(T, 60)
                timer = '{:02d}:{:02d}'.format(mins, secs) 
                print(timer, end="\r") 
                time.sleep(1)
                T -= 1
            await channel.send(f'Как вы Думаете?\nКто Мафия?')
            T = 2
            while T:
               mins, secs = divmod(T, 60)
               timer = '{:02d}:{:02d}'.format(mins, secs) 
               print(timer, end="\r") 
               time.sleep(1)
               T -= 1
            await channel.send('У вас есть 60 секунд, что бы подумать кто мафия\nМафию вибераете через Команду ```$mafia member```')
            T = 60
            while T:
                mins, secs = divmod(T, 60)
                timer = '{:02d}:{:02d}'.format(mins, secs) 
                print(timer, end="\r") 
                time.sleep(1)
                T -= 1
            await channel.send(f'Время истекло\nКак вы думаете?\nКто Мафия?')
        except:
            T = 5
            while T:
                mins, secs = divmod(T, 60)
                timer = '{:02d}:{:02d}'.format(mins, secs) 
                print(timer, end="\r") 
                time.sleep(1)
                T -= 1
            channel = client.get_channel(787344727430397952)
            await channel.send('Наступил День, и город просыпаеться\nЄтой ночю мафия никого не Убила')
            T = 5
            while T:
                mins, secs = divmod(T, 60)
                timer = '{:02d}:{:02d}'.format(mins, secs) 
                print(timer, end="\r") 
                time.sleep(1)
                T -= 1
            await channel.send(f'Как вы Думаете?\nКто Мафия?')
            T = 2
            while T:
                mins, secs = divmod(T, 60)
                timer = '{:02d}:{:02d}'.format(mins, secs) 
                print(timer, end="\r") 
                time.sleep(1)
                T -= 1
            await channel.send('У вас есть 60 секунд, что бы подумать кто мафия\nМафию вибераете через Команду ```$mafia member```')
            T = 60
            while T:
                mins, secs = divmod(T, 60)
                timer = '{:02d}:{:02d}'.format(mins, secs) 
                print(timer, end="\r") 
                time.sleep(1)
                T -= 1
            await channel.send(f'Время истекло\nКак вы думаете?\nКто Мафия?')
    else:
        await ctx.send(f'Доступ к Функции имеет только **MAFIA** !')

@client.command()
async def mafia(ctx, user: discord.Member):
    Users = str(user.mention) + "\n" 
    File = open("Players", "r")
    File_R = open("RolesMafia", "r")
    Players = []
    Roles = []
    for Line in File:
        Players.append(Line)
    for line in File_R:
        Roles.append(line)
    File_R.close()
    File.close()
    Index = Players.index(Users)
    config.index_user = Index
    config.Diference = 1
    await ctx.send("Точно?\nПодумайте хорошо")

@client.command()
async def yes(ctx):
    if config.Diference == 1 and config.Game_is_Started == 1:
        Mafia = open("RolesMafia", "r")
        Players = []
        for Line in Mafia:
            Players.append(Line)
        User_Status = Players[config.index_user]
        config.Diference = 0
        await ctx.send("Окей!\nЭтот игрок был:")
        await ctx.send(User_Status)
        if User_Status != "Mafia":
            #await ctx.send("Но помните, Мафия может Соврать!\nЭто по правилах Класической Мафии")
            config.IsEndTheGame = 1 
        if config.IsEndTheGame == 1:
            File = open("Players", "r+")
            File.truncate(0)
            File.close()
            ListRoles = open("RolesMafia", "r+")
            ListRoles.truncate(0)
            ListRoles.close()
            await ctx.channel.send(f'**Игра Окончана**\nВсе Мафии были найдены:3\nДо Скорых Свтречь')

client.run(config.TOKEN)
