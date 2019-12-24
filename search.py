import  aiohttp
import asyncio
import json
import requests
from db_commands import Com as db


async def fetch(session, url):
    async with session.get(url) as response:
        return await response.json(content_type='text/html')

async def sections(city):
    async with aiohttp.ClientSession() as session:
        html = await fetch(session, f'https://pizzacoffee.by/api/?e=sections&token=1&city={city}')
        result = []
        for key, value in html.items():
            if value["show_main"] == "1":
                result.append(value)
    return result

async def subcat(p_id):
    async with aiohttp.ClientSession() as session:
        w = 350
        html = await fetch(session, f'https://pizzacoffee.by/api/?e=sections&parent={p_id}&token=1')
        result = []
        for key, value in html.items():
            result.append(value)
    return result

async def subcat_pizza(p_id):
    async with aiohttp.ClientSession() as session:
        w = 50
        html = await fetch(session,
                           f'https://pizzacoffee.by/api/?e=products&parent={p_id}&token=1')
        result = []
        keys = []
        print(p_id)
        for key, value in html.items():
            if value == None or value['name'] == None:
                print('NNNN')
            else:
                result.append(value)
                keys.append(key)
    return result, keys

async def more_info_pizza(p_id, c_id):
    async with aiohttp.ClientSession() as session:
        p_id = int(p_id)
        c_id = c_id
        w = 50
        html = await fetch(session, f'https://pizzacoffee.by/api/?e=products&parent={p_id}&token=1')
        result = []
        url = ''
        s = ''
        for keys, value in html.items():
                if keys == str(c_id):
                    url = value['picture']
                    result.append(value['text'])
        for item in result:
            s = item['preview']
    return s, url

async def more_info(p_id, c_id):
    async with aiohttp.ClientSession() as session:
        p_id = int(p_id)
        c_id = c_id
        w = 50
        html = await fetch(session, f'https://pizzacoffee.by/api/?e=products&parent={p_id}&token=1&')
        result = []
        url = ''
        s = ''
        k = c_id
        for keys, value in html.items():
                if keys == str(c_id):
                    url = value['picture']
                    result.append(value['text'])
        for item in result:
            s = item['preview']
        print(s, ': ', url, " : ", k)
    return s, url, k

async def get():
    items, keys = await subcat_pizza(35)
    for value in items:
        print("value:", value['name'])

async def get_city():
    async with aiohttp.ClientSession() as session:
        w = 50
        html = await fetch(session, f'https://pizzacoffee.by/api/?e=city&token=1')
    return html.items()

async def name_i(p_id, c_id):
    async with aiohttp.ClientSession() as session:
        p_id = int(p_id)
        c_id = c_id
        html = await fetch(session, f'https://pizzacoffee.by/api/?e=products&parent={p_id}&token=1')
        name = ''
        for keys, value in html.items():
                if keys == str(c_id):
                    name = value['name']
    return name

async def json_(u_id):
    phone, name, products, items, counts = await db.get_for_json(u_id, loop)
    r = []
    for product, item, count in zip(products, items, counts):
        name = await name_i(product[0], item[0])
        r.append(({"id": item[0], "name": name, "price": 1, "quantity": count[0]}))
    res = json.dumps(r)
    print(res)
    link = f"https://pizzacoffee.by/api/?e=order&login={phone[0]}&password={phone[0]}&username={name[0]}&phone={phone[0]}&products={res}"
    new_link = str(link.replace('[', ''))
    new_link = new_link.replace(']', '')
    print(new_link)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(json_('c8cbqoOqhc9HZTnzF2rX6Q=='))

