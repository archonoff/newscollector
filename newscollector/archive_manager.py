# coding=utf-8

from datetime import datetime

from .yandex_news import YandexSpider


def read_configs(fname):
    configs = __import__(fname)
    return configs.sources


def archive_manager():
    configs = read_configs('sources_dtp_config')
    # start_date = datetime(year=2016, month=6, day=1).date()
    # end_date = datetime(year=2016, month=7, day=1).date()
    # params = {'text': u'дтп'}
    region = 2      # Задание региона поиска
    params = {
        # Задание поисковой строки
        'text': u'дтп',

        # Задание диапазона поиска
        'from_day': '01',
        'from_month': '06',
        'from_year': '2016',
        'to_day': '01',
        'to_month': '07',
        'to_year': '2016',
        'within': '777',        # Константа для поиска по диапазону
    }

    for config in configs:
        source_id = config.get('yandex_news_id')
        enabled = config.get('enabled')
        if not enabled:
            continue
        if source_id:
            for month in range(6, 13):
                if month < 12:
                    params.update({
                        'from_month': '{:0>2}'.format(month),
                        'to_month': '{:0>2}'.format(month+1),
                        'to_year': '2016',
                    })
                else:
                    params.update({
                        'from_month': '{:0>2}'.format(month),
                        'to_month': '01',
                        'to_year': '2017',
                    })
                spider = YandexSpider(config, region, params=params)
                spider.run()            # Вызов синхронный (из-за капчи)
                spider.stop_tor()
            # spider = YandexSpider(config, region, date_span=(start_date, end_date), params=params)
            # spider.run_over_dates()


if __name__ == '__main__':
    archive_manager()
    # todo сделать параметры для запуска через командную строку
