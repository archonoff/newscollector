# coding=utf-8

import re
from time import sleep
from datetime import datetime

from stem.process import launch_tor_with_config
from stem.control import Controller
from stem import Signal

from grab import Grab
from grab.error import GrabNetworkError

from newscollector.newscollector_worker import retrieve_information

'''
https://news.yandex.ru/yandsearch
?geonews=2          регион, 2 - питер
&rpt=nnews2
&nsrc=11826             id источника в базе ЯН
&numdoc=10              выводить на страницу результатов, максимум 50
&p=0                    номер страницы
&from_day=03&from_month=11&from_year=2016&to_day=03&to_month=11&to_year=2016&within=777
'''


# Этот словарь используется, чтобы записывать в базу читаемое название региона
REGIONS = {
    2: "Санкт-Петербург",
    10174: "Ленинградская область",
}


class YandexSpider:
    current_proxy = None
    tor_process = None
    socks_port = 9150
    control_port = 9051
    controller = None
    base_url = 'https://news.yandex.ru'
    next_page_xpath = u'//a[contains(., "Следующая")]/@href'
    links_xpath = '//h2[@class="document__head"]//a/@href'
    captcha_xpath = '//img[@class="image form__captcha"]/@src'
    source_id = None
    start_date = None
    end_date = None

    def __init__(self, config, region, requests_delay=5, params=None, date_span=None):
        """
        :param config: Конфиг-файл сайтов-источников
        :param region: Целове число, представляющее собой регион
        :param requests_delay: Задержка между переходами к следующей странце поиска
        :param params: Словарь. Будет полностью добавлен к строке запроса
        :param date_span: Кортеж (start_date, end_date). На каждый день из заданного промежутка будет создаваться свой запрос. Работает долго, но если новостей много - это единственный выход.
        """
        if params is not None:
            str_params = '&' + '&'.join(['{}={}'.format(k, v) for k, v in params.items()])
        else:
            str_params = ''
        self.str_params = str_params
        self.start_tor()
        self.config = config
        self.name = config.get('name')
        self.url = config.get('url')
        self.source_id = config.get('yandex_news_id')
        self.region_id = region
        self.region_name = REGIONS.get(region)
        self.requests_delay = requests_delay
        if date_span is not None:
            self.start_date = date_span[0]
            self.end_date = date_span[1]

        # Формирование urlа для загрузки
        self.form_url()

    def form_url(self, date=None):
        """Составляет строчку урла. Если передана дата, то дописывает в конец нужные параметры
        :type date: datetime
        :return: None
        """
        start_url = 'https://news.yandex.ru/yandsearch?&rpt=nnews2&numdoc=50&p=0&nsrc={}&geonews={}{}'.format(self.source_id, self.region_id, self.str_params)

        # Установка даты
        if date is not None:
            day = date.day
            month = date.month
            year = date.year
            date_str = '&from_day={day:0>2}&from_month={month:0>2}&from_year={year:0>4}&to_day={day:0>2}&to_month={month:0>2}&to_year={year:0>4}&within=777'.format(day=day, month=month, year=year)
            start_url += date_str

        self.start_url = start_url        # Стартовый url (первая страница)

    def task_news_list_page(self, grab, task):
        """Уже и не помню сам, что тут должно было быть"""
        raise NotImplementedError

    def stop_tor(self):
        """Остановить сервер tor"""
        self.tor_process.kill()

    def start_tor(self):
        """Запуск сервера tor"""
        self.tor_process = launch_tor_with_config(
            config={
                'SocksPort': str(self.socks_port),
                'ControlPort': str(self.control_port),
                # 'GeoIPFile': r'C:\tor-win32-0.2.8.9\Data\Tor\geoip',
                # 'GeoIPv6File': r'C:\tor-win32-0.2.8.9\Data\Tor\geoip6',
                # 'ExitNodes': '{ru}', # если вдруг пригодится
            },
            tor_cmd=r'C:\Users\Oleg\Desktop\tor-win32-0.2.8.9\Tor\tor.exe',
        )
        self.controller = Controller.from_port()
        self.controller.authenticate()

    def change_identity(self):
        """Сменить личность в сети tor"""
        self.controller.signal(Signal.NEWNYM)

    def run_over_dates(self):
        start_day = self.start_date.toordinal()
        end_day = self.end_date.toordinal()
        print('Begin processing dates. Total {} days'.format(end_day - start_day))
        current_day = start_day
        while (end_day - current_day) > 0:
            current_date = datetime.fromordinal(current_day)
            self.form_url(current_date)
            self.run()
            current_day += 1

    def run(self):
        """Запуск процесса сбора с яндекса в бесконечном цикле пока не кончатся ссылки"""
        next_url = self.process_news_list_page(self.start_url)
        i = 0
        while True:
            i += 1
            if not next_url:
                # self.stop_tor()
                break
            print('While loop iteration {}'.format(i))
            next_url = self.process_news_list_page(next_url)

    def process_news_list_page(self, url):
        """Обработка страницы со ссылками на новости"""
        print('Trying open url: {}'.format(url))
        g = Grab(proxy='127.0.0.1:{}'.format(self.socks_port), proxy_type='socks5', timeout=90, connect_timeout=30)
        try:
            g.go(url)
        except GrabNetworkError as e:
            # Ошибка подключения
            print('Connection error: {}'.format(e))
            self.change_identity()               # Используем новую личность
            return url

        # На всякий случай проверим код ответа
        if g.response.code != 200:
            print('Error code: {}'.format(g.response.code))
            self.change_identity()
            return url

        # Проверка, не наткнулись ли мы на капчу
        captcha = g.doc.select(self.captcha_xpath).text_list()
        if captcha:
            print('Captcha found: {}, setting new identity'.format(captcha[0]))
            self.change_identity()               # Используем новую личность
            return url

        # Поиск ссылок на новости
        news_links = g.doc.select(self.links_xpath).text_list()
        for news_link in news_links:
            founded_url = news_link.replace(re.findall('.+//[^/]+', news_link)[0], '')       # Потому что для загрузки надо передавать урл без домена
            pattern = self.config.get('detailed_page_re')
            match = re.search(pattern, founded_url)   # Дополнительная проверка на совпадение полученного урла регулярке
            if match:
                print('Found link: {}, from {}'.format(founded_url, self.url))
                # Передаем в очередь для загрузки
                retrieve_information.apply_async(args=(self.config, founded_url),
                                                 kwargs={'related_from_url': None, 'region': self.region_name},
                                                 priority=251)

        # Поиск ссылки для перехода на следующую страницу
        next_page = g.doc.select(self.next_page_xpath).text_list()
        if next_page:
            if self.requests_delay is not None:
                sleep(self.requests_delay)          # Чтобы не быть слишком настойчивыми
            # Переход на следующую страницу
            return '{}{}'.format(self.base_url, next_page[0])

        # Не было ошибки, и не было найдено ссылки на очередную страницу
        return False
