import logging
import asyncio
from viberbot.api.messages.message import Message
from aioviber.bot import Bot, Api
from aioviber.chat import Chat, Carousel, RichMediaMessage, Keyboard
from aioviber.keyboard import Button
from viberbot.api.viber_requests import ViberSubscribedRequest
import sys
from db_commands import Com as db
import messages as ms
import keyboards as kb
import search
import datetime
from datetime import timedelta
import time


logger = logging.getLogger(__name__)

bot = Bot(
    name='vibertestbot',
    avatar='https://ktonanovenkogo.ru/image/bot-chto-takoe.jpg',
    auth_token="4ab6eddbfae7d3c9-16acc99a2fc10bcf-e816a61fc3011aa9",  # Public account auth token
    host="localhost",  # should be available from wide area network
    port=8000,
    webhook='https://e343428f.ngrok.io',  # Webhook url
)

'''
Для пользователя
'''

'''
Начнало работы
'''

@bot.command('start')
async def start(chat : Chat, matched):
    if await db.user_exist(chat.message.sender.id, loop) == True:
        await chat.send_text(ms.welcome2, keyboard=Keyboard(kb.start, bg_color="#FFFFFF"))
    else:
        await db.add_user(chat.message.sender.id, '', '', '', 'wait_for_city', loop)
        city = await search.get_city()
        keyboard = []
        for key, value in city:
            if key != 'minsk':
                b = Button(action_body=value["name"], columns=6, rows=1, bg_color="#2db9b9", silent=True, action_type="reply",
                       text=value["name"], text_size="regular", text_opacity=60, text_h_align="center", text_v_align="middle")
                keyboard.append(b)
        await chat.send_text(ms.welcome, keyboard=Keyboard(keyboard, bg_color="#FFFFFF"))
        await db.add_user_for_stat(chat.message.sender.id, loop)

@bot.command('старт')
async def start(chat : Chat, matched):
    if await db.user_exist(chat.message.sender.id, loop) == True:
        await chat.send_text(ms.welcome2, keyboard=Keyboard(kb.start, bg_color="#FFFFFF"))
    else:
        await db.add_user(chat.message.sender.id, '', '', '', 'wait_for_city', loop)
        city = await search.get_city()
        keyboard = []
        for key, value in city:
            if key != 'minsk':
                b = Button(action_body=value["name"], columns=6, rows=1, bg_color="#2db9b9", silent=True, action_type="reply",
                           text=value["name"], text_size="regular", text_opacity=60, text_h_align="center", text_v_align="middle")
                keyboard.append(b)
        await chat.send_text(ms.welcome, keyboard=Keyboard(keyboard, bg_color="#FFFFFF"))
        await db.add_user_for_stat(chat.message.sender.id, loop)

'''
Меню, выбор товарар и добвление в корзину
'''

@bot.command('Меню')
async def test(chat: Chat, matched):
    u_id = chat.message.sender.id
    city = await db.get_city(u_id, loop)
    items = await search.sections(city)
    buttons = []
    for item in items:
        image = Button(action_body=f"to-category-{item['id']}", columns=6, rows=5, action_type="reply",
                       image=f"https://pizzacoffee.by/{item['picture']}", text=f'<font color=#323232><b>{item["name"]}</b></font>')

        title_and_text = Button(action_body=f"to-category-{item['id']}", columns=6, rows=1,  action_type="reply",
                                text=f'<font color=#323232><b>{item["name"]}</b></font>', text_size="medium",
                                text_v_align='middle', text_h_align='center')

        buttons.append(image)
        buttons.append(title_and_text)

    results = Carousel(buttons=buttons)

    await chat.send_rich_media(rich_media=results, keyboard=Keyboard(kb.start, bg_color="#FFFFFF"))

@bot.command('to-category-')
async def pizza_cat(chat: Chat, matched):
    u_id = chat.message.sender.id
    category = int(chat.message.message.text[12:])
    buttons = []
    await db.update_more_info(u_id, category, loop)
    subcat = [22, 23, 25]
    i = 0
    items = []
    count = 0
    results =[]
    try:
        items = await search.subcat(category)
        count = len(items)
    except:
        items, keys = await search.subcat_pizza(category)
        count = len(keys)
    if category in subcat:
        if count > 5:
            buttons = []
            for item in items:
                s = item["name"]
                if s == '&quot;Double Pizza&quot; пиццы с двойным сырным дном ':
                    s = 'Пиццы с двойным сырным дном'

                image = Button(action_body=f'to-subcat-{item["id"]}', columns=6, rows=5, action_type="reply",
                               image=f"https://pizzacoffee.by/{item['picture']}")

                title_and_text = Button(action_body=f'to-subcat-{item["id"]}', columns=6, rows=1,
                                        action_type="reply",
                                        text=f'<font color=#323232><b>{s}</b></font>', text_size="medium",
                                        text_v_align='middle', text_h_align='center')

                buttons.append(image)
                buttons.append(title_and_text)

                i += 1
                if len(buttons) == 18 and i < len(items):
                    results = Carousel(buttons=buttons)
                    await chat.send_rich_media(rich_media=results, keyboard=Keyboard(kb.start, bg_color="#FFFFFF"))
                    buttons.clear()
                elif len(buttons) != 18 and i == len(items):
                    results = Carousel(buttons=buttons)
                    await chat.send_rich_media(rich_media=results, keyboard=Keyboard(kb.start, bg_color="#FFFFFF"))
                    buttons.clear()
        else:
            buttons = await kb.to_subcategory(category, loop)
    else:
        i = 0
        if count > 5:
            items, keys = await search.subcat_pizza(category)
            buttons = []
            for item, key in zip(items, keys):
                s = item["name"]

                image = Button(action_body=f'get-more-info-{key}', columns=6, rows=5, action_type="reply",
                               image=f"https://pizzacoffee.by/{item['picture']}")  # resized

                title_and_text = Button(action_body=f'get-more-info-{key}', columns=6, rows=1, action_type="reply",
                                        text=f'<font color=#323232><b>{s}</b></font>', text_size="medium",
                                        text_v_align='middle', text_h_align='left')

                buttons.append(image)
                buttons.append(title_and_text)

                i += 1
                if len(buttons) == 18 and i < len(items):
                    results = Carousel(buttons=buttons)
                    await chat.send_rich_media(rich_media=results, keyboard=Keyboard(kb.start, bg_color="#FFFFFF"))
                    buttons.clear()
                elif len(buttons) != 18 and i == len(items):
                    results = Carousel(buttons=buttons)
                    await chat.send_rich_media(rich_media=results, keyboard=Keyboard(kb.start, bg_color="#FFFFFF"))
                    buttons.clear()
        else:
            buttons = await kb.items_keyboard(category)
    try:
        results = Carousel(buttons=buttons)
        await chat.send_rich_media(rich_media=results, keyboard=Keyboard(kb.start, bg_color="#FFFFFF"))
    except:
        print(0)

@bot.command('to-items-')
async def pizza_cat(chat: Chat, matched):
    u_id = chat.message.sender.id
    category = int(chat.message.message.text[9:])
    buttons = []
    parent_id = await db.get_more_info(u_id, loop)
    items, keys = await search.subcat_pizza(parent_id)
    count = len(keys)
    await db.update_more_info(u_id, category, loop)
    i = 0
    if count > 5:
        for item, key in zip(items, keys):
            s = str(item['name'])
            s = s.replace("&quot;", "'")
            image = Button(action_body=f'get-more-info-{key}', columns=6, rows=5, action_type="reply",
                           image=f"https://pizzacoffee.by/{item['picture_resized']}")  # resized

            title_and_text = Button(action_body=f'get-more-info-{key}', columns=6, rows=1, action_type="reply",
                                    text=f'<font color=#323232><b>{s}</b></font>', text_size="medium",
                                    text_v_align='middle', text_h_align='left')

            buttons.append(image)
            buttons.append(title_and_text)

            i += 1
            if len(buttons) == 18 and i < len(items):
                results = Carousel(buttons=buttons)
                await chat.send_rich_media(rich_media=results, keyboard=Keyboard(kb.start, bg_color="#FFFFFF"))
                buttons.clear()
            elif len(buttons) != 18 and i == len(items):
                results = Carousel(buttons=buttons)
                await chat.send_rich_media(rich_media=results, keyboard=Keyboard(kb.start, bg_color="#FFFFFF"))
                buttons.clear()
    else:
        buttons = await kb.pizza_keyboard(category)
        results = Carousel(buttons=buttons)
        await chat.send_rich_media(rich_media=results, keyboard=Keyboard(kb.start, bg_color="#FFFFFF"))
    try:
        results = Carousel(buttons=buttons)
        await chat.send_rich_media(rich_media=results, keyboard=Keyboard(kb.start, bg_color="#FFFFFF"))
    except:
        print(0)

@bot.command('get-more-info-')
async def get_more_info(chat : Chat, matched):
    u_id = chat.message.sender.id
    category = int(chat.message.message.text[14:])
    parent_id = await db.get_more_info(u_id, loop)
    text, url, key = await search.more_info(parent_id, category)
    button = [Button(action_body=f'add-to-basket-{key}', columns=6, rows=1, action_type="reply",
                     text='<font color=#ffffff>Добавить в корзину</font>', text_size="large", text_v_align='middle',
                     text_h_align='center', bg_color='#2F1AB2')]
    result = Carousel(buttons=button, buttons_group_columns=6, buttons_group_rows=1)
    if len(text) < 2:
        await chat.send_picture('https://pizzacoffee.by/' + url)
        await chat.send_rich_media(rich_media=result)
    else:
        await chat.send_picture('https://pizzacoffee.by/'+url)
        await chat.send_text(text)
        await chat.send_rich_media(rich_media=result, keyboard=Keyboard(kb.start, bg_color="#FFFFFF"))

@bot.command('to-subcat-')
async def to_subcat(chat: Chat, matched):
    u_id = chat.message.sender.id
    category = int(chat.message.message.text[10:])
    buttons = []
    i = 0
    items, keys = await search.subcat_pizza(category)
    count = len(keys)
    if count > 5:
        i = 0
        items, keys = await search.subcat_pizza(category)
        buttons = []
        for item, key in zip(items, keys):
            s = str(item['name'])
            s = s.replace("&quot;", "'")
            image = Button(action_body=f"get-more-info-{key}", columns=6, rows=5, action_type="reply",
                           image=f"https://pizzacoffee.by/{item['picture']}")

            title_and_text = Button(action_body=f"get-more-info-{key}", columns=6, rows=1, action_type="reply",
                                    text=f'<font color=#323232><b>{s}</b></font>', text_size="medium",
                                    text_v_align='middle', text_h_align='left')

            buttons.append(image)
            buttons.append(title_and_text)
            i += 1
            if len(buttons) == 18 and i < len(items):
                results = Carousel(buttons=buttons)
                await chat.send_rich_media(rich_media=results, keyboard=Keyboard(kb.start, bg_color="#FFFFFF"))
                buttons.clear()
            elif len(buttons) != 18 and i == len(items):
                results = Carousel(buttons=buttons)
                await chat.send_rich_media(rich_media=results, keyboard=Keyboard(kb.start, bg_color="#FFFFFF"))
                buttons.clear()
    else:
        buttons = await kb.pizza_keyboard(category)
        results = Carousel(buttons=buttons)
        await chat.send_rich_media(rich_media=results, keyboard=Keyboard(kb.start, bg_color="#FFFFFF"))

@bot.command('add-to-basket-')
async def add(chat: Chat, matched):
    u_id = chat.message.sender.id
    c_id = await db.get_more_info(u_id, loop)
    i_id = int(chat.message.message.text[14:])
    await db.add_item_to_basket(u_id, i_id, c_id, loop)
    button = [Button(action_body=f'otmena', columns=6, rows=1, action_type="reply",
                     text='<font color=#ffffff>Отмена</font>', text_size="large", text_v_align='middle',
                     text_h_align='center', bg_color='#2F1AB2')]
    result = Carousel(buttons=button, buttons_group_columns=6, buttons_group_rows=1)
    await chat.send_text('Какое количество?')
    await chat.send_rich_media(rich_media=result)
    await db.update_context(u_id, f'wait-count', loop)
    await db.update_more_info_c_id(u_id, c_id, loop)

@bot.command('otmena')
async def add(chat: Chat, matched):
    u_id = chat.message.sender.id
    await chat.send_text('Отменено', keyboard=Keyboard(kb.start, bg_color="#FFFFFF"))
    await db.update_context(u_id, '', loop)

'''
Изменение города
'''
@bot.command('change-city')
async def change_city(chat: Chat, matched):
    u_id = chat.message.sender.id
    city = await search.get_city()
    keyboard = []
    for key, value in city:
        if key != 'minsk':
            b = Button(action_body=value["name"], columns=6, rows=1, bg_color="#2db9b9", silent=True, action_type="reply",
                       text=value["name"], text_size="regular", text_opacity=60, text_h_align="center",
                       text_v_align="middle")
            keyboard.append(b)
    keyboard.append(Button(action_body='otmena', columns=6, rows=1, bg_color="#2db9b9", silent=True, action_type="reply",
                   text='<font color=#ffffff>Отмена</font>', text_size="regular", text_opacity=60, text_h_align="center",
                   text_v_align="middle"))
    await chat.send_text(ms.change_city, keyboard=Keyboard(keyboard, bg_color="#FFFFFF"))
    await db.update_context(u_id, f'wait_city', loop)

'''
Работа с корзиной
'''
@bot.command('Корзина')
async def add(chat: Chat, matched):
    u_id = chat.message.sender.id
    categories, items = await db.get_itemd_from_basket(u_id, loop)
    buttons = []
    count = len(items)
    i = 0
    if count != 0:
        if count > 5:
            for category, item in zip(categories, items):
                text, url, key = await search.more_info(category[0], item[0])

                image = Button(action_body=f'none', columns=6, rows=4, action_type="reply",
                               image=f"https://pizzacoffee.by/{url}")

                title_and_text = Button(action_body=f'none', columns=6, rows=1, action_type="reply",
                                        text=f'<font color=#323232><b>{text}</b></font>', text_size="medium",
                                        text_v_align='middle', text_h_align='left')

                delete_from_cart = Button(action_body=f"delete-{item[0]}", columns=6, rows=1, action_type="reply",
                         text=f'Убрать из корзины', text_size="small",
                         text_v_align='middle',
                         text_h_align='center')

                buttons.append(image)
                buttons.append(title_and_text)
                buttons.append(delete_from_cart)
                i += 1
                if len(buttons) == 18 and i < len(items):
                    results = Carousel(buttons=buttons)
                    await chat.send_rich_media(rich_media=results)
                    buttons.clear()
                elif len(buttons) != 18 and i == len(items):
                    results = Carousel(buttons=buttons)
                    await chat.send_rich_media(rich_media=results)
                    buttons.clear()
            button = [Button(action_body=f'none', columns=6, rows=1, action_type="reply",
                             text='<font color=#ffffff>Оформить заказ</font>', text_size="large", text_v_align='middle',
                             text_h_align='center', bg_color='#2F1AB2')]
            result = Carousel(buttons=button, buttons_group_columns=6, buttons_group_rows=1)
            await chat.send_rich_media(rich_media=result, keyboard=Keyboard(kb.start, bg_color="#FFFFFF"))
        else:
            for category, item in zip(categories, items):

                text, url, key = await search.more_info(category[0], item[0])

                image = Button(action_body=f'none', columns=6, rows=4, action_type="open-url",
                               image=f"https://pizzacoffee.by/{url}")  # resized

                title_and_text = Button(action_body=f'none', columns=6, rows=1, action_type="open-url",
                                        text=f'<font color=#323232><b>{text}</b></font>', text_size="medium",
                                        text_v_align='middle', text_h_align='left')

                delete_from_cart = Button(action_body=f"delete-{category[0]}", columns=6, rows=1, action_type="reply",
                                          text=f'Убрать из корзины', text_size="small",
                                          text_v_align='middle',
                                          text_h_align='center')

                buttons.append(image)
                buttons.append(title_and_text)
                buttons.append(delete_from_cart)
            results = Carousel(buttons=buttons)
            await chat.send_rich_media(rich_media=results)
            button = [Button(action_body=f'of-order', columns=6, rows=1, action_type="reply",
                             text='<font color=#ffffff>Оформить заказ</font>', text_size="large", text_v_align='middle',
                             text_h_align='center', bg_color='#2F1AB2')]
            result = Carousel(buttons=button, buttons_group_columns=6, buttons_group_rows=1)
            await chat.send_rich_media(rich_media=result, keyboard=Keyboard(kb.start, bg_color="#FFFFFF"))
    else:
        await chat.send_text('В корзине ничего нет!', keyboard=Keyboard(kb.start, bg_color="#FFFFFF"))

@bot.command('delete-')
async def p(chat: Chat, matched):
    u_id = chat.message.sender.id
    item = chat.message.message.text[7:]
    print(item)
    await db.delete_from_basket(u_id, item, loop)
    await chat.send_text('Товар удален из корзины', keyboard=Keyboard(kb.start, bg_color="#FFFFFF"))


'''
-----------------------------------------------------------------------------------------------------------------------------
'''

'''
Оформление заказа
'''
@bot.command('of-order')
async def ord(chat: Chat, matched):
    u_id = chat.message.sender.id
    await chat.send_text('Введите ваше ФИО:')
    await db.update_context(u_id, 'wait_fio', loop)


'''
Для администратора
'''

@bot.command('/admin')
async def admin(chat: Chat, matched):
    u_id = chat. message.sender.id
    button = [Button(action_body=f'otmena', columns=6, rows=1, action_type="reply",
                     text='<font color=#ffffff>Отмена</font>', text_size="large", text_v_align='middle',
                     text_h_align='center', bg_color='#2F1AB2')]
    result = Carousel(buttons=button, buttons_group_columns=6, buttons_group_rows=1)
    await chat.send_text('Введите пароль')
    await chat.send_rich_media(rich_media=result)
    await db.update_context(u_id, 'wait_password', loop)

'''
Рассылка
'''
@bot.command('send_messages')
async def ras(chat: Chat, matched):
    u_id = chat. message.sender.id
    await chat.send_text('Тип рассылки:',  keyboard=Keyboard(kb.ras, bg_color="#FFFFFF"))

@bot.command('no_orders')
async def ras(chat: Chat, matched):
    u_id = chat. message.sender.id
    no_users = []
    users = await db.get_all_users(loop)
    users_from_orders = await db.users_from_orders(loop)
    for user in users:
        if user in users_from_orders:
            a = 0
        else:
            no_users.append(user)
    if len(no_users) == 0:
        await chat.send_text('Нет таких пользователей', keyboard=Keyboard(kb.ras, bg_color="#FFFFFF"))
    else:
        await chat.send_text('Какой тип сообщения вы хотите отправить?', keyboard=Keyboard(kb.ras_cat, bg_color="#FFFFFF"))
        await db.update_more_info_c_id(u_id, 'no-orders', loop)

@bot.command('one-or-more')
async def ras(chat: Chat, matched):
    u_id = chat. message.sender.id
    users_from_orders = await db.users_from_orders(loop)
    if len(users_from_orders) == 0:
        await chat.send_text('Нет таких пользователей', keyboard=Keyboard(kb.ras, bg_color="#FFFFFF"))
    else:
        await chat.send_text('Какой тип сообщения вы хотите отправить?', keyboard=Keyboard(kb.ras_cat, bg_color="#FFFFFF"))
        await db.update_more_info_c_id(u_id, 'one-or-more', loop)

@bot.command('more-n')
async def ras(chat: Chat, matched):
    u_id = chat. message.sender.id
    users_from_orders = await db.users_from_orders(loop)
    if len(users_from_orders) == 0:
        await chat.send_text('Нет таких пользователей', keyboard=Keyboard(kb.ras, bg_color="#FFFFFF"))
    else:
        await db.update_context(u_id, 'wait_N', loop)
        await chat.send_text('Больше какого количества заказов?')
        await db.update_more_info_c_id(u_id, 'more-n', loop)

@bot.command('m-or-more-month')
async def ras(chat: Chat, matched):
    u_id = chat. message.sender.id
    users_from_orders = await db.users_from_orders(loop)
    if len(users_from_orders) == 0:
        await chat.send_text('Нет таких пользователей', keyboard=Keyboard(kb.ras, bg_color="#FFFFFF"))
    else:
        await db.update_context(u_id, 'wait_N', loop)
        await chat.send_text('Больше какого количества заказов?')
        await db.update_more_info_c_id(u_id, 'm-or-more-month', loop)

@bot.command('sr-sum-more')
async def ras(chat: Chat, matched):
    u_id = chat. message.sender.id
    users_from_orders = await db.users_from_orders(loop)
    if len(users_from_orders) == 0:
        await chat.send_text('Нет таких пользователей', keyboard=Keyboard(kb.ras, bg_color="#FFFFFF"))
    else:
        await db.update_context(u_id, 'wait_N', loop)
        await chat.send_text('Больше какой суммы заказа?')
        await db.update_more_info_c_id(u_id, 'sr-sum-more', loop)

@bot.command('sr-sum-less')
async def ras(chat: Chat, matched):
    u_id = chat. message.sender.id
    users_from_orders = await db.users_from_orders(loop)
    if len(users_from_orders) == 0:
        await chat.send_text('Нет таких пользователей', keyboard=Keyboard(kb.ras, bg_color="#FFFFFF"))
    else:
        await db.update_context(u_id, 'wait_N', loop)
        await chat.send_text('Меньше какой суммы заказа?')
        await db.update_more_info_c_id(u_id, 'sr-sum-less', loop)

@bot.command('pb-n-more')
async def ras(chat: Chat, matched):
    u_id = chat. message.sender.id
    users_from_orders = await db.users_from_orders(loop)
    if len(users_from_orders) == 0:
        await chat.send_text('Нет таких пользователей', keyboard=Keyboard(kb.ras, bg_color="#FFFFFF"))
    else:
        await db.update_context(u_id, 'wait_N', loop)
        await chat.send_text('Больше скольки дней?')
        await db.update_more_info_c_id(u_id, 'pb-n-more', loop)

@bot.command('send-to-all')
async def send_to_all(chat: Chat, matched):
    u_id = chat.message.sender.id
    await chat.send_text('Какой тип сообщения вы хотите отправить?', keyboard=Keyboard(kb.ras_cat, bg_color="#FFFFFF"))
    await db.update_more_info_c_id(u_id, 'one-or-more', loop)

@bot.command('pb-n-less')
async def ras(chat: Chat, matched):
    u_id = chat. message.sender.id
    users_from_orders = await db.users_from_orders(loop)
    if len(users_from_orders) == 0:
        await chat.send_text('Нет таких пользователей', keyboard=Keyboard(kb.ras, bg_color="#FFFFFF"))
    else:
        await db.update_context(u_id, 'wait_N', loop)
        await chat.send_text('Меньше скольки дней?')
        await db.update_more_info_c_id(u_id, 'pb-n-less', loop)

@bot.command('ras-photo')
async def ph(chat: Chat, matched):
    u_id = chat.message.sender.id
    await db.update_context(u_id, 'wait_photo', loop)
    button = [Button(action_body=f'otmena', columns=6, rows=1, action_type="reply",
                     text='<font color=#ffffff>Отмена</font>', text_size="large", text_v_align='middle',
                     text_h_align='center', bg_color='#2F1AB2')]
    result = Carousel(buttons=button, buttons_group_columns=6, buttons_group_rows=1)
    await chat.send_text('Ожидаю картинку')
    await chat.send_rich_media(rich_media=result)

@bot.command('ras-text')
async def ph(chat: Chat, matched):
    u_id = chat.message.sender.id
    await db.update_context(u_id, 'wait_text', loop)
    button = [Button(action_body=f'otmena', columns=6, rows=1, action_type="reply",
                     text='<font color=#ffffff>Отмена</font>', text_size="large", text_v_align='middle',
                     text_h_align='center', bg_color='#2F1AB2')]
    result = Carousel(buttons=button, buttons_group_columns=6, buttons_group_rows=1)
    await chat.send_text('Ожидаю текст')
    await chat.send_rich_media(rich_media=result)

@bot.message_handler('picture')
async def sp(chat: Chat):
    u_id =chat.message.sender.id
    context = await db.get_context(u_id, loop)
    if context == 'wait_photo':
        podcontext = await db.get_more_c_id(u_id, loop)
        if podcontext == 'no-orders':
            no_users = []
            users = await db.get_all_users(loop)
            users_from_orders = await db.users_from_orders(loop)
            for user in users:
                if user in users_from_orders:
                    a = 0
                else:
                    no_users.append(user)
            for user in no_users:
                await chat.send_picture_plus(picture=chat.message.message.media, to=str(user))
            await chat.send_text(f'Количество отправленных сообщений: {len(no_users)}', keyboard=Keyboard(kb.ras_cat, bg_color="#FFFFFF"))
            await db.update_more_info_c_id(u_id, 0, loop)
        elif podcontext == 'one-or-more':
            users_from_orders = await db.users_from_orders(loop)
            for user in users_from_orders:
                await chat.send_picture_plus(picture=chat.message.message.media, to=str(user))
            await chat.send_text(f'Количество отправленных сообщений: {len(users_from_orders)}', keyboard=Keyboard(kb.ras_cat, bg_color="#FFFFFF"))
            await db.update_more_info_c_id(u_id, 0, loop)
        elif podcontext == 'more-n':
            n = await db.get_more_info(u_id, loop)
            res =[]
            users_from_orders = await db.users_from_orders(loop)
            for user in users_from_orders:
                sum = await db.users_from_orders_more_n(user, int(n[0]), loop)
                if sum != None and int(sum[0]) >=int(n[0]):
                    res.append(user)
            if len(res) != 0:
                for user in res:
                    await chat.send_picture_plus(picture=chat.message.message.media, to=str(user))
                await chat.send_text(f'Количество отправленных сообщений: {len(res)}', keyboard=Keyboard(kb.ras_cat, bg_color="#FFFFFF"))
                await db.update_more_info_c_id(u_id, 0, loop)
            else:
                await chat.send_text('Нет таких пользователей', keyboard=Keyboard(kb.ras_cat, bg_color="#FFFFFF"))
        elif podcontext == 'm-or-more-month':
            date_now = datetime.date.today()
            n = await db.get_more_info(u_id, loop)
            res =[]
            users_from_orders = await db.users_from_orders(loop)
            for user in users_from_orders:
                sum = await db.users_from_orders_more_n_and_date(user, int(n[0]), loop)
                if sum != None and int(sum[0]) >=int(n[0]):
                    res.append(user)
            if len(res) != 0:
                for user in res:
                    await chat.send_picture_plus(picture=chat.message.message.media, to=str(user))
                await chat.send_text(f'Количество отправленных сообщений: {len(res)}', keyboard=Keyboard(kb.ras_cat, bg_color="#FFFFFF"))
                await db.update_more_info_c_id(u_id, 0, loop)
            else:
                await chat.send_text('Нет таких пользователей', keyboard=Keyboard(kb.ras_cat, bg_color="#FFFFFF"))
        elif podcontext == 'sr-sum-more':
            date_now = datetime.date.today()
            n = await db.get_more_info(u_id, loop)
            res =[]
            users_from_orders = await db.users_from_orders(loop)
            for user in users_from_orders:
                sum = await db.users_from_orders_more_n_sum(user, int(n[0]), loop)
                if sum != None and float(sum) >=float(n[0]):
                    res.append(user)
            if len(res) != 0:
                for user in res:
                    await chat.send_picture_plus(picture=chat.message.message.media, to=str(user))
                await chat.send_text(f'Количество отправленных сообщений: {len(res)}', keyboard=Keyboard(kb.ras_cat, bg_color="#FFFFFF"))
                await db.update_more_info_c_id(u_id, 0, loop)
            else:
                await chat.send_text('Нет таких пользователей', keyboard=Keyboard(kb.ras_cat, bg_color="#FFFFFF"))
        elif podcontext == 'sr-sum-less':
            date_now = datetime.date.today()
            n = await db.get_more_info(u_id, loop)
            res = []
            users_from_orders = await db.users_from_orders(loop)
            for user in users_from_orders:
                sum = await db.users_from_orders_less_n_sum(user[0], int(n[0]), loop)
                if sum != None and float(sum) <= float(n):
                    res.append(user)
            if len(res) != 0:
                for user in res:
                    await chat.send_picture_plus(picture=chat.message.message.media, to=str(user))
                await chat.send_text(f'Количество отправленных сообщений: {len(res)}', keyboard=Keyboard(kb.ras_cat, bg_color="#FFFFFF"))
                await db.update_more_info_c_id(u_id, 0, loop)
            else:
                await chat.send_text('Нет таких пользователей', keyboard=Keyboard(kb.ras_cat, bg_color="#FFFFFF"))
        elif podcontext == 'pb-n-more':
            date_now = datetime.date.today()
            n = await db.get_more_info(u_id, loop)
            res = []
            users_from_orders = await db.users_from_orders_more_n_date(n, loop)
            if users_from_orders != None:
                for user in users_from_orders:
                    await chat.send_picture_plus(picture=chat.message.message.media, to=str(user))
                await chat.send_text(f'Количество отправленных сообщений: {len(users_from_orders)}', keyboard=Keyboard(kb.ras_cat, bg_color="#FFFFFF"))
                await db.update_more_info_c_id(u_id, 0, loop)
            else:
                await chat.send_text('Нет таких пользователей', keyboard=Keyboard(kb.ras_cat, bg_color="#FFFFFF"))
                await db.update_more_info_c_id(u_id, 0, loop)
        elif podcontext == 'pb-n-less':
            date_now = datetime.date.today()
            n = await db.get_more_info(u_id, loop)
            res = []
            users_from_orders = await db.users_from_orders_less_n_date(n, loop)
            if  users_from_orders != None:
                for user in users_from_orders:
                        await chat.send_picture_plus(picture=chat.message.message.media, to=str(user))
                await chat.send_text(f'Количество отправленных сообщений: {len(users_from_orders)}', keyboard=Keyboard(kb.ras_cat, bg_color="#FFFFFF"))
                await db.update_more_info_c_id(u_id, 0, loop)
            else:
                await chat.send_text('Нет таких пользователей', keyboard=Keyboard(kb.ras_cat, bg_color="#FFFFFF"))
                await db.update_more_info_c_id(u_id, 0, loop)
        elif podcontext == 'send-to-all':
            all_users = await db.get_all_users(loop)
            for user in all_users:
                await chat.send_picture_plus(picture=chat.message.message.media, to=str(user))
            await chat.send_text(f'Количество отправленных сообщений: {len(all_users)}',
                                 keyboard=Keyboard(kb.ras_cat, bg_color="#FFFFFF"))
            await db.update_more_info_c_id(u_id, 0, loop)


'''
------------------------------------------------------------------------------------------------------------------------
'''
'''
Работа с контекстом
'''
@bot.default('')
async def default(chat : Chat):
    if await db.user_exist(chat.message.sender.id, loop) == False:
        await chat.send_text('Для начала работы с ботом необходимо написать Старт или Start')
    else:
        u_id = chat.message.sender.id

        context = await db.get_context(u_id, loop)
        city = await search.get_city()
        if context == 'wait_for_city':
            await chat.send_text(f'Ваш город: {chat.message.message.text}.\nБей по кнопкам!', keyboard=Keyboard(kb.start,bg_color="#FFFFFF"))
            for key, value in city:
                if value["name"] == chat.message.message.text:
                    await db.update_city(u_id, key, loop)
                    await db.update_context(u_id, ' ', loop)
        elif context == 'wait-count':
            count = chat.message.message.text
            if count.isdigit():
                await chat.send_text('Товар добавлен в корзину!',  keyboard=Keyboard(kb.start, bg_color="#FFFFFF"))
                c_id = await db.get_more_c_id(u_id, loop)
                await db.update_count_to_basket(u_id, c_id, count, loop)
                await db.update_context(u_id, '', loop)
                await db.update_more_info_c_id(u_id, 0, loop)
            else:
                await chat.send_text('Пожалуйста введите целое число:')
        elif context == 'wait_password':
            password = chat.message.message.text
            if password == ms.PASSWORD:
                await chat.send_text('Добро пожаловать!', keyboard=Keyboard(kb.adim_kb, bg_color="#FFFFFF"))
                await db.update_context(u_id, '', loop)
            else:
                await chat.send_text('Неверный пароль! Повторите попытку ввода')
        elif context == 'wait_city':
            city = await search.get_city()
            await chat.send_text(f'Ваш город изменен на: {chat.message.message.text}.\nБей по кнопкам!',
                                 keyboard=Keyboard(kb.start, bg_color="#FFFFFF"))
            for key, value in city:
                if value["name"] == chat.message.message.text:
                    await db.update_city(u_id, key, loop)
                    await db.update_context(u_id, ' ', loop)
        elif context == 'wait_N':
            await db.update_more_info(u_id, int(chat.message.message.text), loop)
            await chat.send_text('Какой тип сообщения вы хотите отправить?',
                                 keyboard=Keyboard(kb.ras_cat, bg_color="#FFFFFF"))

        elif context == 'wait_text':
            podcontext = await db.get_more_c_id(u_id, loop)
            if podcontext == 'no-orders':
                no_users = []
                users = await db.get_all_users(loop)
                users_from_orders = await db.users_from_orders(loop)
                for user in users:
                    if user in users_from_orders:
                        a = 0
                    else:
                        no_users.append(user)
                for user in no_users:
                    await chat.send_text_plus(to=str(u_id), text=chat.message.message.text)
                await chat.send_text(f'Количество отправленных сообщений: {len(no_users)}', keyboard=Keyboard(kb.ras_cat, bg_color="#FFFFFF"))
                await db.update_more_info_c_id(u_id, 0, loop)
            if podcontext == 'one-or-more':
                users_from_orders = await db.users_from_orders(loop)
                for user in users_from_orders:
                    await chat.send_text_plus(to=str(u_id), text=chat.message.message.text)
                await chat.send_text(f'Количество отправленных сообщений: {len(users_from_orders)}', keyboard=Keyboard(kb.ras_cat, bg_color="#FFFFFF"))
                await db.update_more_info_c_id(u_id, 0, loop)
            elif podcontext == 'more-n':
                n = await db.get_more_info(u_id, loop)
                res = []
                users_from_orders = await db.users_from_orders(loop)
                for user in users_from_orders:
                    sum = await db.users_from_orders_more_n(user, int(n[0]), loop)
                    if sum != None and int(sum[0]) >= int(n[0]):
                        res.append(user)
                if len(res) != 0:
                    for user in res:
                        await chat.send_text_plus(to=str(u_id), text=chat.message.message.text)
                    await chat.send_text(f'Количество отправленных сообщений: {len(res)}', keyboard=Keyboard(kb.ras_cat, bg_color="#FFFFFF"))
                    await db.update_more_info_c_id(u_id, 0, loop)
                else:
                    await chat.send_text('Нет таких пользователей', keyboard=Keyboard(kb.ras_cat, bg_color="#FFFFFF"))
            elif podcontext == 'm-or-more-month':
                date_now = datetime.date.today()
                n = await db.get_more_info(u_id, loop)
                res = []
                users_from_orders = await db.users_from_orders(loop)
                for user in users_from_orders:
                    sum = await db.users_from_orders_more_n_and_date(user, int(n[0]), loop)
                    if sum != None and int(sum[0]) >= int(n[0]):
                        res.append(user)
                if len(res) != 0:
                    for user in res:
                        await chat.send_text_plus(to=str(u_id), text=chat.message.message.text)
                    await chat.send_text(f'Количество отправленных сообщений: {len(res)}', keyboard=Keyboard(kb.ras_cat, bg_color="#FFFFFF"))
                    await db.update_more_info_c_id(u_id, 0, loop)
                else:
                    await chat.send_text('Нет таких пользователей', keyboard=Keyboard(kb.ras_cat, bg_color="#FFFFFF"))
            elif podcontext == 'sr-sum-more':
                date_now = datetime.date.today()
                n = await db.get_more_info(u_id, loop)
                res = []
                users_from_orders = await db.users_from_orders(loop)
                for user in users_from_orders:
                    sum = await db.users_from_orders_more_n_sum(user, int(n[0]), loop)
                    if sum != None and float(sum) >= float(n[0]):
                        res.append(user)
                if len(res) != 0:
                    for user in res:
                        await chat.send_text_plus(to=str(u_id), text=chat.message.message.text)
                    await chat.send_text(f'Количество отправленных сообщений: {len(res)}', keyboard=Keyboard(kb.ras_cat, bg_color="#FFFFFF"))
                    await db.update_more_info_c_id(u_id, 0, loop)
                else:
                    await chat.send_text('Нет таких пользователей', keyboard=Keyboard(kb.ras_cat, bg_color="#FFFFFF"))
            elif podcontext == 'sr-sum-less':
                date_now = datetime.date.today()
                n = await db.get_more_info(u_id, loop)
                res = []
                users_from_orders = await db.users_from_orders(loop)
                for user in users_from_orders:
                    sum = await db.users_from_orders_less_n_sum(user, int(n[0]), loop)
                    if sum != None and float(sum) <= float(n):
                        res.append(user)
                if len(res) != 0:
                    for user in res:
                        await chat.send_text_plus(to=str(u_id), text=chat.message.message.text)
                    await chat.send_text(f'Количество отправленных сообщений: {len(res)}', keyboard=Keyboard(kb.ras_cat, bg_color="#FFFFFF"))
                    await db.update_more_info_c_id(u_id, 0, loop)
                else:
                    await chat.send_text('Нет таких пользователей', keyboard=Keyboard(kb.ras_cat, bg_color="#FFFFFF"))
            elif podcontext == 'pb-n-less':
                date_now = datetime.date.today()
                n = await db.get_more_info(u_id, loop)
                res = []
                users_from_orders = await db.users_from_orders_less_n_date(n, loop)
                if users_from_orders != None:
                    for user in users_from_orders:
                        await chat.send_text_plus(to=str(u_id), text=chat.message.message.text)
                    await chat.send_text(f'Количество отправленных сообщений: {len(users_from_orders)}', keyboard=Keyboard(kb.ras_cat, bg_color="#FFFFFF"))
                    await db.update_more_info_c_id(u_id, 0, loop)
                else:
                    await chat.send_text('Нет таких пользователей', keyboard=Keyboard(kb.ras_cat, bg_color="#FFFFFF"))
                    await db.update_more_info_c_id(u_id, 0, loop)
            elif podcontext == 'pb-n-more':
                date_now = datetime.date.today()
                n = await db.get_more_info(u_id, loop)
                res = []
                users_from_orders = await db.users_from_orders_more_n_date(n, loop)
                if users_from_orders != None:
                    for user in users_from_orders:
                        await chat.send_text_plus(to=str(u_id), text=chat.message.message.text)
                    await chat.send_text(f'Количество отправленных сообщений: {len(users_from_orders)}', keyboard=Keyboard(kb.ras_cat, bg_color="#FFFFFF"))
                    await db.update_more_info_c_id(u_id, 0, loop)
                else:
                    await chat.send_text('Нет таких пользователей', keyboard=Keyboard(kb.ras_cat, bg_color="#FFFFFF"))
                    await db.update_more_info_c_id(u_id, 0, loop)
            elif podcontext == 'send-to-all':
                all_users = await db.get_all_users(loop)
                for user in all_users:
                    await chat.send_text_plus(to=str(u_id), text=chat.message.message.text)
                await chat.send_text(f'Количество отправленных сообщений: {len(all_users)}',
                                     keyboard=Keyboard(kb.ras_cat, bg_color="#FFFFFF"))
                await db.update_more_info_c_id(u_id, 0, loop)
        elif context == 'wait_fio':
            fio = chat.message.message.text
            await db.update_fio(u_id, fio, loop)
            await chat.send_text('Спасибо! Теперь введите ваш номер телефона:')
            await db.update_context(u_id, 'wait_tel', loop)
        elif context == 'wait_tel':
            tel = chat.message.message.text
            await db.update_tel(u_id, tel, loop)
            await db.update_context(u_id, '', loop)
            await chat.send_text('Ваш заказ оформлен, ожидайте звонка оператора.')

        elif context == 'wait_start_date':
            date = chat.message.message.text
            try:
                date = time.strptime(date, '%Y-%m-%d')
                await db.update_context(u_id, 'wait_finish_date', loop)
                await db.update_more_info(u_id, date, loop)
                await chat.send_text('Введите дату конца отчетного периода в формате ГГГГ-ММ-ДД')
            except ValueError:
                await chat.send_text('Вы ввели неправильный формат даты. Введите пожалуйста в таком формате: ГГГГ-ММ-ДД')
        elif context == 'wait_finish_date':
            f_date = chat.message.message.text
            try:
                f_date = time.strptime(f_date, '%Y-%m-%d')
                await db.update_context(u_id, '', loop)
                s_date = await db.get_more_info(u_id, loop)
                new_users = await db.get_cont_new_users(s_date, f_date, loop)
                out_users = await db.get_cont_out_users(s_date, f_date, loop)
                count_orders = await db.get_cont_orders(s_date, f_date, loop)
                city = ['baranovichi', 'bobruysk', 'volkovisk', 'grodno', 'zhlobin', 'slutsk', 'vitebsk']
                c_count =[]
                for c in city:
                    p = await db.get_users_city(c, loop)
                    c_count.append(p[0])
                text = f'Статистика по периоду:\n' \
                    f'\n-Новые пользователи: {new_users[0]};' \
                    f'\n-Ушедшие пользователи: {out_users[0]};' \
                    f'\n-Кол-во оформленных заказов: {count_orders[0]};'
                text_2 =  f'Кол-во пользователей по городам:'\
                f'\n -Барановичи:{c_count[0]};' \
                    f'\n -Бобруйск:{c_count[1]};' \
                    f'\n -Волковыск:{c_count[2]};' \
                    f'\n -Гродно:{c_count[3]};' \
                    f'\n -Жлобин:{c_count[4]};' \
                    f'\n -Слуцк:{c_count[5]};' \
                    f'\n -Витебск:{c_count[6]};'

                await chat.send_text(text)
                await chat.send_text(text_2)
            except ValueError:
                await chat.send_text(
                    'Вы ввели неправильный формат даты. Введите пожалуйста в таком формате: ГГГГ-ММ-ДД')
        else:
            await chat.send_text('Приступай к покупкам!', keyboard=Keyboard(kb.start, bg_color="#FFFFFF"))

'''
Для статистики
'''

@bot.command('stat-')
async def stat(chat: Chat, matched):
    u_id= chat.message.sender.id
    await chat.send_text('Введите дату начала отчетного периода в формате ГГГГ-ММ-ДД')
    await db.update_context(u_id, 'wait_start_date', loop)

@bot.event_handler('unsubscribed')
async def ev(matched):
    u_id = await bot.api.get_account_info()
    u_id = u_id['members']
    u_id = u_id[0]
    u_id = u_id['id']
    await db.update_user_for_stat(u_id, loop)

loop = asyncio.get_event_loop()
if __name__ == '__main__':  # pragma: no branch
    import aiohttp.web
    aiohttp.web.run_app(bot.app, host=bot.host, port=bot.port)