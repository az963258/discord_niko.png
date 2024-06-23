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
import logging

with open(u"./config.json", "r") as file:
    config = load(file)

#steam = Steam(config["SteamApiToken"])


bot = commands.InteractionBot()

#wapi.set_lang('ru')

logging.basicConfig(level=logging.INFO, filename="logs.log", format='%(asctime)s | %(levelname)s | %(message)s', encoding='utf-8')

@bot.event
async def on_ready():
    print("ботяра готов")
    logging.info('бот запущен')


# кастомизация?
main_color = disnake.Color.from_rgb(188, 49, 99)

#эмбед ошибки
async def error_embed(inter, error):
    embed = disnake.Embed(title='❌ Ой...', description=f'🔍 Возникла ошибка, подробности: `{error}`', color=main_color)
    await inter.send(embed=embed)
    print(f'Ошибка! | {error}')
    logging.error(error)


@bot.slash_command(name="пинг", description='Выводит в чат задержку')
async def user(inter):
    logging.info(f'Команда "пинг" отправлена, отправитель: {inter.author}')
    try:
        await inter.send(embed=disnake.Embed(title='❗ Понг!', description=f'🛜 Задержка: {bot.latency*1000:.2f} мс',  colour=main_color))
    except Exception as e:
        await error_embed(inter, e)


@bot.message_command(name="Ревёрс")
async def reverse(inter: disnake.ApplicationCommandInteraction, message: disnake.Message):
    logging.info(f'Команда "Ревёрс" отправлена, отправитель: {inter.author}')
    try:
        await inter.response.send_message(f"{message.content[::-1]}\n{message.jump_url}")
    except Exception as e:
        await error_embed(inter, e)

@bot.slash_command(name='вики-поиск', description='Ищет информацию на википедии')
async def wikisearch(inter, запрос:str):
    try:
        await inter.send('В переработке')
    except Exception as e:
        await error_embed(inter, e)
    #await inter.response.defer()
    #sentences = 6
    ##try:
    #page = wapi.page(запрос)
    #if len(page.summary) > 4000:
    #    sentences = 4
    #await inter.edit_original_response(embed=disnake.Embed(title=f'Результат на запрос "{запрос}"',description=page.summary(sentences=sentences)))
    ##except Exception as e:
    #    #await inter.edit_original_response(embed=disnake.Embed(title=f'Ошибка!', description=e))

@bot.slash_command(name='кот', description='Кот. Просто выводит рандомную пикчу кота')
async def catpicture(inter):
    logging.info(f'Команда "кот" отправлена, отправитель: {inter.author}')
    
    await inter.response.defer()

    try:
        response = requests.get("https://some-random-api.com/animal/cat")
        data = response.json()

        if response.status_code == 200:
            image_url = data["image"]
            image = requests.get(image_url)

        bytes = io.BytesIO(image.content)

        await inter.send(file=disnake.File(bytes, filename='kot.jpg'))
    except Exception as e:
        await error_embed(inter, e)

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
    logging.info(f'Команда "анонимное-сообщение" отправлена, отправитель: {inter.author}')
    try:
        await inter.send("Молодец! Ты прочитал это сообщение! Гордись собой что-ли", ephemeral=True)
        channel = inter.channel
        await inter.delete_original_response()
        await channel.send(сообщение)
        print(f'Анон сообщение | "{сообщение}" от {inter.author}')
        logging.info(f'Анон сообщение | "{сообщение}" от {inter.author}')
    except Exception as e:
        await error_embed(inter, e)

@bot.slash_command(name='рандом', description='Выводит рандомное число в указанном диапазоне')
async def randomchislo(inter, диапазон:int):
    logging.info(f'Команда "рандом" отправлена, отправитель: {inter.author}')
    try:
        if диапазон <= 0:
            await inter.send(embed = disnake.Embed(title='Эй!', description='Диапазон не может быть равен или быть меньше нуля.', color=main_color), ephemeral=True)
        else:
            embed = disnake.Embed(title=f'Твоё число: {random.randint(1, диапазон)}', color=main_color)
            await inter.send(embed=embed)
    except Exception as e:
        await error_embed(inter, e)

@bot.slash_command(name='fakenitro-эмоджи', description='Генерирует ссылку на FakeNitro эмоджи')
async def fakenitrogen(inter, эмоджи:str):
    logging.info(f'Команда "fakenitro-эмоджи" отправлена, отправитель: {inter.author}')
    try:
        emoji = disnake.PartialEmoji.from_str(эмоджи)
        if emoji.url == '':
            await inter.send(embed=disnake.Embed(title='Неправильный формат эмоджи', description='Ссылка на эмоджи пустая', color=main_color))
        else:
            embed = disnake.Embed(title='Твоя FakeNitro ссылка на эмоджи', description=f"`[{emoji.name}]({emoji.url})`", color=main_color)
            await inter.send(embed=embed)
    except Exception as e:
        await error_embed(inter, e)

@bot.slash_command(name='ошибка', description='вызывает эмбед ошибки с заданым типом ошибки')
async def raiseaerror(inter):
    logging.info(f'Команда "ошибка" отправлена, отправитель: {inter.author}')
    try:
        raise SyntaxError("вызвано пользователем")
    except Exception as e:
        await error_embed(inter, e)


@bot.user_command(name="Информация о юзере")
async def userinfo(inter: disnake.ApplicationCommandInteraction, user: disnake.User):

    logging.info(f'Команда "Информация о юзере" отправлена, отправитель: {inter.author}')
    
    isBot = None
    isOwner = None
    dopinfo = "нету"

    try:
        if user.bot == True:
            isBot = "Да"
        else:
            isBot = 'Нет'

        if user.id == 669577742924251159:
            isOwner = 'Да'
            dopinfo = 'если вы не поняли, то это кодер бота'
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

        if user.id == 885576438646972496: #sionit_1337
            dopinfo = 'Сионитовое сияние чистого гнева'

        if user.id == 1056407095605469214: #abstractdevs
            dopinfo = 'чебурек быстрого ответа'

        embed=disnake.Embed(title=f'Информация о {user.display_name}',colour=main_color, description=f'📛 Оторбражаемое имя: {user.display_name}\n🔰 Никнейм: {user.name}\n🔢 Айди: {user.id}\n🔤 Ссылка: <https://discord.com/users/{user.id}>\n🤖 Является ли ботом?: {isBot}\n🔧 Является ли моим создателем?: {isOwner}\n📝 Дополнительная информация: {dopinfo}')
        embed.set_image(url=user.avatar.url)

        await inter.response.send_message(embed=embed, components=[disnake.ui.Button(label='🪪 Открыть аватарку', style=disnake.ButtonStyle.url, url=user.avatar.url)])
    except Exception as e:
        await error_embed(inter, e)


bot.run(config["Token"])
