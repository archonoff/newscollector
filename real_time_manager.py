# coding=utf-8

from time import sleep
from threading import Thread

from newscollector.newscollector_worker import search_index
from newscollector.db_functions import add_source_if_missed


def read_configs(fname):
    configs = __import__(fname)
    return configs.sources


def index_check_runner(config):
    """
    Поток для периодической проверки главной страницы новостного сайта
    """
    delay = config.get('refresh_delay')
    url = config.get('url')
    while True:
        # Запуска задачи просмотра главной страницы, и после ее завершения запуск задачи загрузки найденных ссылок
        print('Launch index task for {}'.format(url))
        # следующую очередь запускать с высочайшим приоритетом
        search_index.apply_async(args=(config,), priority=255)
        sleep(delay)


def real_time_manager():
    configs = read_configs('sources_config')
    for config in configs:
        # todo сделать на каждый источник по очереди celery и по воркеру
        enabled = config.get('enabled')
        if not enabled:
            continue

        # проверка списка источников и добавление отсутствующих
        add_source_if_missed(config)

        # Запуск потока для постоянной проверки
        Thread(target=index_check_runner, args=(config, )).start()


if __name__ == '__main__':
    real_time_manager()
