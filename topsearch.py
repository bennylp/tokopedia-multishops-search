#!/usr/bin/env python

import json
import os
import sys
import time

from bs4 import BeautifulSoup as bs
import requests


bike_shops = {
    "hospecialty": 5554437,
    "hobbyone": 244797,
    "sepeda98": 257358,
    "charliebikeshop": 1758316,
    "charliebikeshop2": 9097897,
    "velocycle": 2143789,
    "spin-warriors": 480498,
    "bragabike": 9170164,
    "velospeed": 7893143,
    "technobike": 1230145,
    "trzbik": 9392621,
    "tkbike (mahal bisa sampe 25%)": 7152778,
    "bikecorpsurabaya": 4458922,
    "bikecenter (lebih mahal 10-20%)": 5397991,  # lebih mahal (303s 24jt)
    "maxxiebike01": 9127557,  # asesoris kecil2
    "bitesnbikes": 5937186,
    "collincycling (agak mahal)": 2445583,  # agak mahal (303s 22.5jt)
    "rizkylbf": 2557713,
    "overflow7": 2537227,
    "elvesbikeid": 9525691,
    "bikebikeajaid": 9673127,
    "lunalabobike": 9287351,
    "klass": 9068286, # agak mahal (r8020 18.5jt)
    
    # parts
    "phjazz-lapak (kediri)": 1204958,
    "sgsbike (lbh mahal ~25%)": 8758036,
    "istimewabike (murah)": 6282811,
    "original-zone": 135665,
    "klarinda (murah)": 8725993,
};

#bike_shops = {"klarinda": 8725993,}

garmin_shops = {
    "garmin": 0,
}


def multi_shops_search(shops, keywords):
    orig_keywords = keywords
    keywords = keywords.strip().replace(' ', '+')
    print(f"Keywords: {keywords}")
    html_out = f'''<!doctype html>
<html lang="en">
<body style="font-family: arial; font-size: medium;">
<p>Searching for: {orig_keywords}</p>
    '''

    headers = {'User-Agent':'Mozilla/5.0 (X11; Linux x86_64; rv:74.0) Gecko/20100101 Firefox/74.0'}
    nresults = 0
    
    for shop_name, shop_id in shops.items():
        if not shop_id:
            url = 'https://tokopedia.com/' + shop_name
            req = requests.post(url, headers=headers, timeout=5)
            req.raise_for_status()

            sup = bs(req.text, 'html.parser')
            for i in sup.find_all('meta', attrs={'name':'branch:deeplink:$android_deeplink_path'}):
                shop_id = i.get('content')[5:]
                if shop_id:
                    print(f"{shop_name} {shop_id}")
                    break
        if not shop_id:
            assert not "Shop id not found"
        time.sleep(0.5)

        url = f'https://ace.tokopedia.com/search/product/v3?q={keywords}&shop_id={shop_id}&rows=80&start=0&full_domain=www.tokopedia.com&scheme=https&device=desktop&source=shop_product'
        req = requests.get(url, headers=headers)
        doc = req.json()
        products = doc['data']['products']
        print(f'{shop_name}: {len(products)} result(s)')
        nresults += len(products)
        if len(products):
            html_out += f'<p><i>Got {len(products)} result(s) from {shop_name}</i></p>\n\n'
            html_out += "<table>\n"
        
        for product in products:
            html_out += """
            <tr>\n"""
            html_out += f"""
            <td>
                <img src='{product["image_url_300"]}' width=120 height=120>
            </td>\n"""
            html_out += f"""
            <td>
                <a href="{product['url']}">{product['name']}</a><BR>
                <strong>{product['price']}</strong><BR>
                Rating: {product['rating']}<BR>
                {product['count_sold']+'<BR>' if 'count_sold' in product else ''}
            </td>
            """
            html_out += """
            </tr>\n"""
        html_out += "</table>\n"
    
    html_out += '''</body></html>'''
    
    if nresults:
        if not os.path.exists('output'):
            os.mkdir('output')
        fname = f'output/{orig_keywords}.html'
        with open(fname, 'wt') as f:
            f.write(html_out)
        
        os.system(f'xdg-open "{fname}"')
    else:
        print('Not found..')


if __name__ == '__main__':
    keywords = ' '.join(sys.argv[1:])
    if keywords:
        multi_shops_search(bike_shops, keywords)

