# coding=utf-8

import requests
import re
import logging

from celery import Celery
from grab import Grab

from newscollector.db_functions import get_news_from_db, add_news, add_relation
from newscollector.settings import CELERY_BACKEND, CELERY_BROKER, PROCESS_RECURSIVE_LINKS, PROCESS_RELATED_LINKS

app = Celery('newscollector.newscollector_worker', backend=CELERY_BACKEND, broker=CELERY_BROKER)

# app = Celery(config_source='celeryconfig')

l = logging.getLogger()


@app.task
def retrieve_information(config, url, related_from_url=None, region=None):
    """
    Получает на вход конфиг и урл и извлекает данные согласно схеме в конфиге

    :param config: Конфиг по данному источнику
    :param url: Относительная ссылка на конкретную новость, начинается с /
    :param related_from_url: Тут будет url новости, с которой стояла ссылка на данную.
        Обязательно с того же самого источника, иначе функция get_news_from_db() не найдет ее
    :param region: Название региона, которая будет записана в базу данных

    :type config: dict
    :type url: str
    :type related_from_url: str | None
    :type region: str | None
    :rtype: bool
    """
    # Получение нужных данных из конфига
    base_url = config.get('url')

    print('processing url {}{}'.format(base_url, url))

    # Проверка, не добавлена ли уже новость в БД
    existing_news = get_news_from_db(config, url)
    if existing_news is not None and related_from_url is None:
        # Новость уже есть в БД и добавлять нечего
        return
    elif existing_news is not None and related_from_url is not None:
        # Новость есть в БД, но возможно на нее можно поставить ссылку
        if related_from_url in [news.news_url for news in existing_news.relations]:
            # Если для данного url уже стоит ссылка с related_from_url
            return
        else:
            # Если нашлась новая связанная новость
            add_relation(to_news=existing_news, from_news=get_news_from_db(config, related_from_url))
            print('we have been added relation, from {}, to {}'.format(related_from_url, url))

        # Больше ничего не требуется, так как новость уже существует, можно просто завершить задачу
        return

    # Получение нужных данных из конфига
    pattern = config.get('detailed_page_re')

    grab = Grab(timeout=90, connect_timeout=30)
    grab.go('{}{}'.format(base_url, url))

    if grab.response.code == 404:
        print('url returned 404 {}{}'.format(base_url, url))
        return

    print('adding url {}{}'.format(base_url, url))
    add_news(config, url, grab, related_from_url, region)

    related_links_filtered = []
    if PROCESS_RELATED_LINKS:
        # Получение связанных новостей, проверка их соответствию шаблону ссылок и передача этой ссылки загрузчику
        related_xpath = config.get('related')
        if related_xpath:
            related_links = grab.doc.select(related_xpath).text_list()
            link_re = re.compile(pattern)
            # todo в следующей строчке может быть ошибочное совпадение, если на другом сайте структура урла совпрадет с данным регулярным выражением
            related_links_filtered = [match.group() for related_link in related_links for match in [link_re.search(related_link)] if match]
            for related_link in related_links_filtered:
                # следующий таск с пониженным приоритетом
                retrieve_information.apply_async(args=(config, related_link, url), priority=100)    # Передача текущего url'а, как источника

    if PROCESS_RECURSIVE_LINKS:
        # Получение рекурсивных ссылок на другие новости с текущей страницы и запуск для них process_links
        recursive_links = set(re.findall(pattern, str(grab.doc.body))) - {url} - set(related_links_filtered)
        for link in recursive_links:
            # следующие таски запускать с минимальным приоритетом
            retrieve_information.apply_async(args=(config, link), priority=10)


@app.task
def search_index(config):
    """
    Функция просматривает главную страницу сайта и извлекает список ссылок на новости
    :type config: dict
    :rtype: list
    """
    url = config.get('url')
    pattern = config.get('detailed_page_re')
    index_page = requests.get(url, verify=False).text
    news_links = set(re.findall(pattern, index_page))
    for link in list(news_links):
        # следующие таски запускать с высоким приоритетом
        retrieve_information.apply_async(args=(config, link), priority=250)


@app.task
def process_links(links, config):
    """
    Функция получает список ссылок на новости и запускает для каждой ссылки задачу retrieve_information
    """
    for link in links:
        retrieve_information.delay(config, link)
        # retrieve_information(config, link)
