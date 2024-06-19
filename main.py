import json

import disnake
from json import load
from disnake.ext import commands
import random
import asyncio
#import wikipedia as wapi
import requests
import io
import os
#from steam_web_api import Steam

with open(u"./config.json", "r") as file:
    config = load(file)

#steam = Steam(config["SteamApiToken"])


bot = commands.InteractionBot()

#wapi.set_lang('ru')

@bot.event
async def on_ready():
    print("мыша готова")


@bot.slash_command(name="пинг", description='Выводит в чат задержку')
async def user(inter):
    await inter.send(embed=disnake.Embed(title='❗ Понг!', description=f'`🛜 Задержка: {bot.latency*1000:.2f} мс`',  colour=disnake.Color.from_rgb(188, 49, 99)))


@bot.message_command(name="Ревёрс")
async def reverse(inter: disnake.ApplicationCommandInteraction, message: disnake.Message):
    await inter.response.send_message(f"{message.content[::-1]}\n{message.jump_url}")

@bot.slash_command(name='вики-поиск', description='Ищет информацию на википедии')
async def wikisearch(inter, запрос:str):
    await inter.send('В переработке')
    #await inter.response.defer()
    #sentences = 6
    ##try:
    #page = wapi.page(запрос)
    #if len(page.summary) > 4000:
    #    sentences = 4
    #await inter.edit_original_response(embed=disnake.Embed(title=f'Результат на запрос "{запрос}"',description=page.summary(sentences=sentences)))
    ##except Exception as e:
    #    #await inter.edit_original_response(embed=disnake.Embed(title=f'Ошибка!', description=e))

@bot.slash_command(name='отправить-идею', description='Скоро устареет')
async def sendidea(inter, идея:str):
    channel = bot.get_channel(1231328113800253540)
    await channel.send(f'Новая идея!\n`{идея}`')
    await inter.send('Идея успешно отправлена!', ephemeral=True)

@bot.slash_command(name='кот', description='Кот. Просто выводит рандомную пикчу кота')
async def catpicture(inter):
    await inter.response.defer()
    response = requests.get("https://some-random-api.com/animal/cat")
    data = response.json()

    if response.status_code == 200:
        image_url = data["image"]
        image = requests.get(image_url)

    bytes = io.BytesIO(image.content)
    await inter.send(file=disnake.File(bytes, filename='kot.jpg'))

@bot.slash_command(name='стим-юзер', description='Выполняет поиск юзера в стиме')
async def steamusersearch(inter, ник:str):
    await inter.send("В переработке")
    #vivod = steam.users.search_user(ник)
    #games_massive = []
    #recent_games = steam.users.get_user_recently_played_games(vivod["player"]["steamid"])
    ##for game in range(recent_games["total_count"]):
    #for game in range(5):
    #    this_game = recent_games['games'][game]
    #    this_game_name = this_game["name"]
    #    games_massive.append(this_game_name)

    #games_in_total = ", ".join(games_massive)

    #embedd = disnake.Embed(title=f"Информация о {vivod['player']['personaname']}",
    #                       description=f"Айди: {vivod['player']["steamid"]}\n[Ссылка]({vivod['player']["profileurl"]})\nКод страны: {vivod["player"]["loccountrycode"]}\nПоследние 5 игр: {games_in_total}")
    #embedd.set_image(vivod["player"]["avatarfull"])
    #await inter.send(embed=embedd)

@bot.slash_command(name='анонимное-сообщение', description="Отправляет сообщение от имени бота")
async def anonimus(inter, сообщение:str):
    churka_message = random.choice(['пшол нах', '⚠☢CHURKA DETECTED⚠☢', '🙌', 'неа', 'нельзя', 'чурькам ввод запрещён', 'катись нахуй', 'поплачь', '"вот тебе паяльник, запаяй себе ебальник"'])
    
    if inter.author.id == 1242475166483878000:
        await inter.send(сообщение)
    else:
        await inter.send("Сообщение-болванка", ephemeral=True)
        channel = inter.channel
        await channel.send(сообщение)
        await inter.delete_original_response()
        print(f'Анон сообщение| "{сообщение}" от {inter.author}')








@bot.user_command(name="Информация о юзере")
async def userinfo(inter: disnake.ApplicationCommandInteraction, user: disnake.User):

    isBot = None
    isOwner = None
    dopinfo = "нету"

    if user.bot == True:
        isBot = "Да"
    else:
        isBot = 'Нет'

    if user.id == 669577742924251159:
        isOwner = 'Да'
    else:
        isOwner = 'Нет'

    if user.id == 1242475166483878000: #tvoy.furka
        dopinfo = 'животное, гадина, чурька, 17% доброты, темни'

    if user.id == 1090144651111059567: #flaful_zzz...
        dopinfo = 'как хочешь'

    if user.id == 909825566969045083: #бабахавод
        dopinfo = 'тостер xd'

    if user.id == 1137277749258629150: #жопеир
        dopinfo = '"добряк с мохнатой попкой" - AbstractDevs'

    embed=disnake.Embed(title=f'Информация о {user.display_name}',colour=disnake.Color.from_rgb(188, 49, 99) , description=f'📛 Оторбражаемое имя: {user.display_name}\n🔰 Никнейм: {user.name}\n🔢 Айди: {user.id}\n🔤 Ссылка: <https://discord.com/users/{user.id}>\n🤖 Является ли ботом?: {isBot}\n🔧 Является ли моим создателем?: {isOwner}\n📝 Дополнительная информация: {dopinfo}')
    embed.set_image(url=user.avatar.url)

    await inter.response.send_message(embed=embed)


bot.run(config["Token"])
