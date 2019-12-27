# -*- coding: utf-8 -*-
from aioviber import Keyboard, Button
import search

start = [Button(action_body="Меню", columns=6, rows=1, bg_color="#2db9b9", silent=True, action_type="reply", text='Меню', text_size= "regular", text_opacity=60, text_h_align="center", text_v_align= "middle"),
         Button(action_body="Вопросы и ответы", columns=3, rows=1, bg_color="#2db9b9", silent=True, action_type="reply", text='Вопросы и ответы', text_size= "regular", text_opacity=60, text_h_align="center", text_v_align= "middle"),
         Button(action_body="change-city", columns=3, rows=1, bg_color="#2db9b9", silent=True, action_type="reply", text='Изменить город', text_size= "regular", text_opacity=60, text_h_align="center", text_v_align= "middle"),
         Button(action_body="Корзина", columns=6, rows=1, bg_color="#2db9b9", silent=True, action_type="reply", text='Корзина', text_size= "regular", text_opacity=60, text_h_align="center", text_v_align= "middle")]

adim_kb= [Button(action_body="send_messages", columns=6, rows=1, bg_color="#2db9b9", silent=True, action_type="reply", text='Сделать рассылку', text_size= "regular", text_opacity=60, text_h_align="center", text_v_align= "middle"),
         Button(action_body="stat-", columns=6, rows=1, bg_color="#2db9b9", silent=True, action_type="reply", text='Статистика', text_size= "regular", text_opacity=60, text_h_align="center", text_v_align= "middle"),
         Button(action_body="otmena", columns=6, rows=1, bg_color="#2db9b9", silent=True, action_type="reply", text='Назад', text_size= "regular", text_opacity=60, text_h_align="center", text_v_align= "middle")]

ask_kb = [Button(action_body="Контакты", columns=6, rows=1, bg_color="#2db9b9", silent=True, action_type="reply", text='Контакты', text_size= "regular", text_opacity=60, text_h_align="center", text_v_align= "middle"),
         Button(action_body="Условия доставки", columns=6, rows=1, bg_color="#2db9b9", silent=True, action_type="reply", text='Условия доставки', text_size= "regular", text_opacity=60, text_h_align="center", text_v_align= "middle"),
         Button(action_body="Способы оплаты", columns=6, rows=1, bg_color="#2db9b9", silent=True, action_type="reply", text='Способы оплаты', text_size= "regular", text_opacity=60, text_h_align="center", text_v_align= "middle"),
Button(action_body="Клубная карта", columns=6, rows=1, bg_color="#2db9b9", silent=True, action_type="reply",
       text='Клубная карта', text_size="regular", text_opacity=60, text_h_align="center", text_v_align="middle"),
          Button(action_body="otmena", columns=6, rows=1, bg_color="#2db9b9", silent=True, action_type="reply",
                 text='Назад', text_size="regular", text_opacity=60, text_h_align="center",
                 text_v_align="middle")]

card = [Button(action_body="Почему стоит приобрести нашу клубную карту", columns=6, rows=1, bg_color="#2db9b9", silent=True, action_type="reply", text='Почему стоит приобрести нашу клубную карту?', text_size= "regular", text_opacity=60, text_h_align="center", text_v_align= "middle"),
        Button(action_body="КАК ОНА РАБОТАЕТ?", columns=6, rows=1, bg_color="#2db9b9", silent=True, action_type="reply",
               text='ЧТО ТАКОЕ КЛУБНАЯ КАРТА И КАК ОНА РАБОТАЕТ?', text_size="regular", text_opacity=60, text_h_align="center",
               text_v_align="middle"),
        Button(action_body="КАКОВА МАКСИМАЛЬНАЯ СКИДКА, КОТОРУЮ ВЫ МОЖЕТЕ ПОЛУЧИТЬ С ПОМОЩЬЮ КАРТЫ", columns=6, rows=1, bg_color="#2db9b9", silent=True, action_type="reply",
               text='КАКОВА МАКСИМАЛЬНАЯ СКИДКА, КОТОРУЮ ВЫ МОЖЕТЕ ПОЛУЧИТЬ С ПОМОЩЬЮ КАРТЫ?', text_size="regular", text_opacity=60, text_h_align="center",
               text_v_align="middle"),
        Button(action_body="КАК МНЕ ПРИОБРЕСТИ КЛУБНУЮ КАРТУ", columns=6, rows=1, bg_color="#2db9b9", silent=True, action_type="reply",
               text='КАК МНЕ ПРИОБРЕСТИ КЛУБНУЮ КАРТУ?', text_size="regular", text_opacity=60, text_h_align="center",
               text_v_align="middle"),
        Button(action_body="СМОГУ ЛИ Я ИСПОЛЬЗОВАТЬ КАРТУ", columns=6, rows=1, bg_color="#2db9b9", silent=True, action_type="reply", text='СМОГУ ЛИ Я ИСПОЛЬЗОВАТЬ КАРТУ, ЕСЛИ ЗАБЫЛ ЕЕ ДОМА, ЛИШЬ НАЗВАВ СВОЕ ИМЯ?', text_size= "regular", text_opacity=60, text_h_align="center", text_v_align= "middle"),
         Button(action_body="КАК УЗНАТЬ", columns=6, rows=1, bg_color="#2db9b9", silent=True, action_type="reply", text='КАК УЗНАТЬ, СКОЛЬКО БАЛЛОВ У МЕНЯ УЖЕ ЕСТЬ?', text_size= "regular", text_opacity=60, text_h_align="center", text_v_align= "middle"),
          Button(action_body="otmena", columns=6, rows=1, bg_color="#2db9b9", silent=True, action_type="reply",
                 text='Назад', text_size="regular", text_opacity=60, text_h_align="center",
                 text_v_align="middle")]


ras = [Button(action_body="no_orders", columns=6, rows=1, bg_color="#2db9b9", silent=True, action_type="reply", text='Нет заказов', text_size= "regular", text_opacity=60, text_h_align="center", text_v_align= "middle"),
         Button(action_body="one-or-more", columns=6, rows=1, bg_color="#2db9b9", silent=True, action_type="reply", text='1 или более заказов', text_size= "regular", text_opacity=60, text_h_align="center", text_v_align= "middle"),
         Button(action_body="more-n", columns=6, rows=1, bg_color="#2db9b9", silent=True, action_type="reply", text='Более N кол-ва заказов', text_size= "regular", text_opacity=60, text_h_align="center", text_v_align= "middle"),
         Button(action_body="m-or-more-month", columns=6, rows=1, bg_color="#2db9b9", silent=True, action_type="reply", text='N или более заказов за последний месяц', text_size= "regular", text_opacity=60, text_h_align="center", text_v_align= "middle"),
       Button(action_body="sr-sum-more", columns=6, rows=1, bg_color="#2db9b9", silent=True, action_type="reply",
              text='Средняя сумма заказов больше N', text_size="regular", text_opacity=60, text_h_align="center",
              text_v_align="middle"),
Button(action_body="sr-sum-less", columns=6, rows=1, bg_color="#2db9b9", silent=True, action_type="reply",
              text='Средняя сумма заказов меньше N', text_size="regular", text_opacity=60, text_h_align="center",
              text_v_align="middle"),
Button(action_body="pb-n-less", columns=6, rows=1, bg_color="#2db9b9", silent=True, action_type="reply",
              text='Пользуются ботом меньше N дней', text_size="regular", text_opacity=60, text_h_align="center",
              text_v_align="middle"),
Button(action_body="pb-n-more", columns=6, rows=1, bg_color="#2db9b9", silent=True, action_type="reply",
              text='Пользуются ботом больше N дней', text_size="regular", text_opacity=60, text_h_align="center",
              text_v_align="middle"),
Button(action_body="send-to-all", columns=6, rows=1, bg_color="#2db9b9", silent=True, action_type="reply",
              text='Всем пользователям', text_size="regular", text_opacity=60, text_h_align="center",text_v_align="middle"),
       Button(action_body="otmena", columns=6, rows=1, bg_color="#2db9b9", silent=True, action_type="reply",
              text='Назад', text_size="regular", text_opacity=60, text_h_align="center", text_v_align="middle")]



ras_cat = [Button(action_body="ras-photo", columns=6, rows=1, bg_color="#2db9b9", silent=True, action_type="reply",
              text='Картинка', text_size="regular", text_opacity=60, text_h_align="center", text_v_align="middle"),
           Button(action_body="ras-text", columns=6, rows=1, bg_color="#2db9b9", silent=True, action_type="reply",
                  text='Текст', text_size="regular", text_opacity=60, text_h_align="center", text_v_align="middle"),
Button(action_body="otmena", columns=6, rows=1, bg_color="#2db9b9", silent=True, action_type="reply",
              text='Назад', text_size="regular", text_opacity=60, text_h_align="center", text_v_align="middle")
           ]


async def items_keyboard(category):
    items, keys = await search.subcat_pizza(category)
    buttons = []
    for item, key in zip(items, keys):
        s = item["name"]

        image = Button(action_body=f"get-more-info-{key}", columns=6, rows=5, action_type="reply",
                       image=f"https://pizzacoffee.by/{item['picture']}")

        title_and_text = Button(action_body=f"get-more-info-{key}", columns=6, rows=1, action_type="reply",
                                text=f'<font color=#323232><b>{s}</b></font>', text_size="medium",
                                text_v_align='middle', text_h_align='left')


        buttons.append(image)
        buttons.append(title_and_text)

    return buttons

async def to_subcategory(category,loop):
    items = await search.subcat(category)
    buttons = []
    for item in items:
        s = item["name"]
        if s == '&quot;Double Pizza&quot; пиццы с двойным сырным дном ':
            s = 'Пиццы с двойным сырным дном'

        image = Button(action_body=f'to-subcat-{item["id"]}', columns=6, rows=5, action_type="reply",
                       image=f"https://pizzacoffee.by/{item['picture']}")

        title_and_text = Button(action_body=f'to-subcat-{item["id"]}', columns=6, rows=1, action_type="reply",
                                text=f'<font color=#323232><b>{s}</b></font>', text_size="medium",
                                text_v_align='middle', text_h_align='center')
        buttons.append(image)
        buttons.append(title_and_text)

    return buttons

async def pizza_keyboard(p_id):
    items, keys = await search.subcat_pizza(p_id)
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
    return buttons
