import requests
import json
from tqdm import tqdm


class ParseAtomicHub:

    def __init__(self):
        self.wax_params = json.load(open(r'setting/wax.json', 'r'))
        self.headers = json.load(open(r'setting/head.json', 'r'))
        self.params = json.load(open(r'setting/param.json', 'r'))

    def price_wax_usdt(self):

        """Получаем курс WAX/USDT с Binance"""

        response = requests.get('https://www.binance.com/api/v1/aggTrades', params=self.wax_params).json()

        return float(response[0].get('p'))

    def low_price(self):

        """Возвращает список цен по возрастающей в долларах"""

        # Отправляет запрос
        response = requests.get('https://wax.api.aa.atomichub.io/atomicmarket/v2/sales', params=self.params,
                                headers=self.headers).json()

        # Возвращает низкие цены по возрастанию и указывает какая валюта
        price_nft = [
            (price.get('listing_price')[: -2] + '.' + price.get('listing_price')[-2:], price.get('listing_symbol'))
            for
            price in response.get('data')]

        usd_token = list()

        # Получаю когда разделять доллар
        for price_wax in price_nft:
            if price_wax[1] == 'USD':
                l = price_wax[0].split('.')
                break

        # Меняю все ваксы на баксы
        for price in tqdm(price_nft, desc='Processing', position=0, miniters=1):
            if price[1] == 'WAX':
                refact = str(self.price_wax_usdt() * float(price[0]))[:-2]
                done = refact[: len(l[0])] + '.' + refact[len(l[0]): len(l[0]) + 2]
                usd_token.append(done)
            else:
                usd_token.append(price[0])

        # Конвертирую список в float из str
        float_list_usd_token = list(map(float, usd_token))

        # Сортирую по возрастанию
        float_list_usd_token.sort()

        return float_list_usd_token


if __name__ == '__main__':
    p = ParseAtomicHub()
    print(p.low_price())