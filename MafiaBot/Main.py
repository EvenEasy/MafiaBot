import config
from time import sleep
import time
import discord
import json
from discord.ext import commands
from discord.utils import get
import random

client = commands.Bot(command_prefix='$')

@client.event
async def on_ready():
    print(f'[{time.time()}] Bot is Connected!')
    with open("data_seince.json", 'r') as file:
        data = json.load(file)
    data["GameInfo"]["Quantity Mafias"] = 0
    data["GameInfo"]["Is End"] = False
    data["GameInfo"]["Is Started"] = False
    data["GameInfo"]["Quantity Players"] = 0
    del data['Players']
    data["Players"] = {}
    del data['Players Mention']
    data["Players Mention"] = {}
    with open("data_seince.json", 'w') as file:
        json.dump(data, file, indent=4)
    
@client.event
async def on_member_join(member : discord.Member):
    channel = client.get_channel(779697732746739712)
    await channel.send(member.mention + " :grey_exclamation: **Welcome**")
    #await member.send(":grey_exclamation: Hey **Welcome*\nI'm Emma\nMore : ```$help```")

@client.command()#aliases = ['set_up', 'commands']
async def _help(ctx):
    await ctx.author.send(f'**Привет)))**\nЯ Emma, и я Мафия БОТ:3\nвот Список Комманд')
    emd = discord.Embed(title='Commands:')

    emd.add_field(name = '{}join'.format('$'), value='Присоединиться к Игре')
    emd.add_field(name = '{}unjoin'.format('$'), value='Покинуть Игру')
    emd.add_field(name = '{}start'.format('$'), value='Начать Игру')
    emd.add_field(name = '{}card'.format('$'), value='Забрать свою Карточку')
    emd.add_field(name = '{}mafia <member mention>'.format('$'), value='Отпределиться кто Мафия')
    emd.add_field(name = '{}yes'.format('$'), value='Подтвердить!')
    emd.add_field(name = '{}go'.format('$'), value='Еслы уже все взяли карточку!')
    emd.add_field(name = '{}kill <member mention>'.format('$'), value='Убить, но если указать большое число чем можно, то никого не Убит')
    emd.add_field(name = '{}clear <message>'.format('$'), value='Очистка чата')

    await ctx.author.send(embed = emd)

@client.command()
async def clear(ctx, amount = 100):
    await ctx.channel.purge(limit = amount)
    await ctx.send("Было очищано: **{}**сообщений".format(amount))
    time.sleep(1)
    await ctx.channel.purge(limit = 1)


@client.command()
async def join(ctx):#registers at game
    with open("data_seince.json", "r") as file:
        data = json.load(file)
    if data["GameInfo"]["Is Started"] == False:
        channel_game = client.get_channel(787344727430397952)
        if str(ctx.author.mention) in data['Players']:
            await ctx.send(f'Вы уже есть в списке Игроков, ожидайте игру на канале {channel_game.mention}\nв Голосовом канале - https://discord.gg/C6Ur68Wnws')
        elif str(ctx.author.mention) not in data['Players']:
            role = get(ctx.author.guild.roles, name="Player🃏")
            data["Players"][str(ctx.author.mention)] = "people"
            data["Players Mention"][str(ctx.author)] = str(ctx.author.mention)
            data["GameInfo"]["Quantity Players"] += 1
            with open("data_seince.json","w") as file:
                json.dump(data, file, indent=4)
            QP = data["GameInfo"]["Quantity Players"]
            await ctx.author.add_roles(role)
            print(f'[User: {ctx.author}] in game!')
            await ctx.send(f'Я вас добавила в Список играков, ожидайте начало игры на канале {channel_game.mention}\nИ тут - https://discord.gg/C6Ur68Wnws')
            await ctx.send(f"Количество Играков: **{QP}**\nНеобходимо минимум 5 **Учасников**")
    else:
        QP = data["GameInfo"]["Quantity Players"]
        await ctx.send(f'{ctx.author.mention} Игра уже началась,\nОжидайте следуещей игры!\n:3')
        await ctx.send(f"Количество Играков: **{QP}**\nНеобходимо минимум 5 **Учасников**")

@client.command()
async def unjoin(ctx):
    with open("data_seince.json", "r") as file:
        data = json.load(file)
    if data["GameInfo"]["Is Started"] == False and str(ctx.author.mention) in data['Players']:
        role = get(ctx.author.guild.roles, name="Player🃏")
        await ctx.author.remove_roles(role)
        del data['Players'][str(ctx.author.mention)]
        del data['Players Mention'][str(ctx.author)]
        del data["Players Org"][str(ctx.author)]
        data["GameInfo"]["Quantity Players"] -= 1
        with open("data_seince.json","w") as file:
            json.dump(data, file, indent=4)
        await ctx.send(f'Вы уже не учасник Игры')
    else:
        await ctx.send(f'Вас нет в Списке играков')

@client.command()
async def start(ctx):#game start
    with open("data_seince.json", "r") as file:
        data = json.load(file)
    if data["GameInfo"]["Is Started"] == False and data["GameInfo"]["Quantity Players"] > 4:
        data["GameInfo"]["Is Started"] = True
        channel_game = client.get_channel(787344727430397952)
        await channel_game.send(f'Ничинаем!')
        await channel_game.send(f'Чтобы забрать свою карточку, напишите команду ```$card```')
        Players = []
        for name in data["Players"].keys():
            Players.append(name)
        mafia = 0
        if len(Players) >= 2:
            mafia = random.randint(0, len(Players))
        data["Players"][Players[mafia]] = "Mafia"
        data["GameInfo"]["Quantity Mafias"] += 1
        with open("data_seince.json", 'w') as file:
            json.dump(data, file, indent=4)
        await ctx.send(f'Ок, я Стартую игру\nИгра на {channel_game.mention}!')        
    else:
        await ctx.send('Ожидайте остольных игроков, Пожалуйста:3')

@client.command()
async def card(ctx):#get a card
    with open("data_seince.json", "r") as file:
        data = json.load(file)
    if data["GameInfo"]["Is Started"]:
        if data["Players"][str(ctx.author.mention)] == "Mafia":
            await ctx.author.send('Вы: **{}**'.format(data["Players"][str(ctx.author.mention)]))
            await ctx.author.send('Чтобы выбрать жертву, напишите ```$kill <Member mention>```\nвот список играков:')
            for Player in data["Players Mention"].keys():
                await ctx.author.send('Player: {0}\n'.format(Player))
        else:
            await ctx.author.send('Вы: **{}**'.format(data["Players"][str(ctx.author.mention)]))
    else:
        await ctx.send('Игра ищё не началась!')

@client.command()
async def go(ctx):
    await ctx.channel.send(f'Начимаем **!**')
    sleep(15)
    await ctx.send('     **Night**    \nГород засыпает!')
    
    sleep(5)
    await ctx.send("Просипаеться **Мафия**")
    sleep(10)
    await ctx.send(f'Мафия виберает **Жертву**')

@client.command()
async def kill(ctx, member):
    with open("data_seince.json", "r") as file:
        data = json.load(file)
    server = discord.Server(id='779680079995076618')
    selected = str(data["Players Mention"][member])
    imMafia = data["Players Mention"][str(ctx.author)]
    if data["Players"][imMafia] == "Mafia":
        try:

            sleep(5)
            
            role = get(member.guild.roles, name="Player🃏")
            await member.remove_roles(role)
            channel = client.get_channel(787344727430397952)
            del data["Players"][selected]
            with open("data_seince.json", 'w') as file:
                json.dump(data, file, indent=4)
            await channel.send('Игрок: {}\nБыл Убит Мафией'.format(selected))

            sleep(5)

            await channel.send(f'Как вы Думаете?\nКто Мафия?')

            sleep(5)

            await channel.send('У вас есть 60 секунд, что бы подумать кто мафия\nМафию вибераете через Команду ```$mafia member```')
            
            sleep(5)

            await channel.send(f'Время истекло\nКак вы думаете?\nКто Мафия?')
        except:

            sleep(5)

            channel = client.get_channel(787344727430397952)
            await channel.send('Наступил **День**, и город **просыпаеться**\nЄтой ночю мафия никого не Убила')

            sleep(5)

            await channel.send(f'Как вы Думаете?\nКто Мафия?')
            sleep(5)
            await channel.send('У вас есть 60 секунд, что бы подумать кто мафия\nМафию вибераете через Команду ```$mafia member```')
            
            sleep(60)

            await channel.send(f'Время истекло\nКак вы думаете?\nКто Мафия?')
    else:
        await ctx.send(f'Доступ к Функции имеет только **MAFIA** !')

@client.command()
async def mafia(ctx, user: discord.Member):
    with open("data_seince.json", "r") as file:
        data = json.load(file)
    data["GameInfo"]["Selected"] = data["Players Mention"][str(user)]
    with open("data_seince.json", 'w') as file:
        json.dump(data, file, indent=4)
    await ctx.send("Точно?\nПодумайте хорошо")

@client.command()
async def yes(ctx):
    with open("data_seince.json", "r") as file:
        data = json.load(file)
    if data["GameInfo"]["Is Started"]:
        await ctx.send("Окей!\nЭтот игрок был:")
        await ctx.send(data['Players'][data['Players']["Selected"]])
        if data['Players'][data['GameInfo']["Selected"]] == "Mafia":
            del data["Players"][data['GameInfo']["Selected"]]
            data['GameInfo']["Selected"] = None
            data["GameInfo"]["Quantity Mafias"] -= 1
            data["GameInfo"]["Quantity Players"] -= 1
            if data["GameInfo"]["Quantity Mafias"] <= 0:
                data["GameInfo"]["Quantity Mafias"] = 0
                data["GameInfo"]["Is End"] = True 
        if data["GameInfo"]["Is End"]:
            data["GameInfo"]["Is End"] = False
            data["GameInfo"]["Is Started"] = False
            datadata["GameInfo"]["Quantity Players"] = 0
            for line in data["Players"].keys():
                user_id = int(((str(line).replace("<", '')).replace(">", '')).replace("!", ''))
                user = ctx.utils.get_member(user_id)
                del data['Players'][user]
            with open("data_seince.json", 'w') as file:
                json.dump(data, file, indent=4)
            await ctx.channel.send(f'**Игра Окончана**\nВсе Мафии были найдены:3\nДо Скорых Свтречь')

client.run(config.TOKEN)