welcome = 'Привет! В каком городе ты живешь?'

welcome2 = 'Привет! Рад твоему возвращению'

change_city = 'Выбери город:'

PASSWORD = '1234567890'
'''
        elif context == "pizza_category":

            p_id = chat.message.message.text
            p_id = p_id[10:]
            i = 0
            if p_id != '35':
                results = Carousel(buttons=buttons)
                await chat.send_rich_media(rich_media=results)
                buttons.clear()
            if p_id == '35':
                items, keys = await search.subcat_pizza(p_id)
                buttons = []
                for item, key in zip(items, keys):
                    s = str(item['name'])
                    s = s.replace("&quot;", "'")
                    if item != 'None' or item != None:
                        image = Button(action_body="https://www.google.com", columns=6, rows=4, action_type="open-url",
                                       image=f"https://pizzacoffee.by/{item['picture']}")

                        title_and_text = Button(action_body="https://www.google.com", columns=6, rows=1,
                                                action_type="open-url",
                                                text=f'<font color=#323232><b>{s}</b></font>', text_size="medium",
                                                text_v_align='middle', text_h_align='left')

                        add = Button(action_body=f"Подробнее {key}", columns=6, rows=1, action_type="reply",
                                     text=f'<font color=#ffffff>Подробнее</font>', text_size="large",
                                     text_v_align='middle',
                                     text_h_align='left',
                                     image='https://cdn.pixabay.com/photo/2012/04/02/16/07/button-24843_1280.png')

                        buttons.append(image)
                        buttons.append(title_and_text)
                        buttons.append(add)
                        i += 1
                        if len(buttons) == 18 and i < len(items):
                            results = Carousel(buttons=buttons)
                            await chat.send_rich_media(rich_media=results)
                            buttons.clear()
                        elif len(buttons) != 18 and i == len(items):
                            results = Carousel(buttons=buttons)
                            await chat.send_rich_media(rich_media=results)
                            buttons.clear()
            await db.update_more_info(u_id, p_id, loop)
            await db.update_context(u_id, 'more_info_pizza', loop)



'''