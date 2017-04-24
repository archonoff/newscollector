# coding=utf-8

# todo добавить в конфиг базовую ссылку для регионального поиска (для заданного региона)


sources = [
            # Вести
            {
                # Основные данные по новостному ресурсу
                'enabled': False,
                'name': 'Вести',
                'url': 'http://www.vesti.ru',
                'test_urls': ['http://www.vesti.ru/doc.html?id=2878282'],
                'yandex_news_id': 1102,

                'refresh_delay': 600,

                # Некоторый шаблон для поиска ссылки на страницу новости
                'detailed_page_re': '/doc.html\?id=[0-9]{7}',

                # Дальше лежат данные по аттрибутам для извлечения
                'attributes_text': {
                    'title': '//h3[@class="article__title"]',
                    'text': '//div[@class="article__text"]//p',
                },
                'attributes_relations': {
                    'date': '//div[@class="article__date"]/text()[1]',
                },

                'related': '//div[@class="more-news"]/ul/li/h4/a/@href',
            },

            # Медуза
            {
                # Основные данные по новостному ресурсу
                'enabled': False,
                'name': 'Медуза',
                'url': 'https://meduza.io',
                'test_urls': ['https://meduza.io/news/2017/04/16/erdogan-dobilsya-pobedy-na-referendume-on-smozhet-ostatsya-u-vlasti-do-2029-goda'],
                'yandex_news_id': 254119998,

                'refresh_delay': 600,                # Частота проверки главной (в секундах)

                # Некоторый шаблон для поиска ссылки на страницу новости
                'detailed_page_re': '/news/[0-9]{4}/[0-9]{1,2}/[0-9]{1,2}/[-\w]+',

                # Дальше лежат данные по аттрибутам для извлечения
                'attributes_text': {
                    'title': '//h1[@class="NewsMaterialHeader-title"]',           # xpath для извлечения данных
                    'text': '//div[@class="Body"]//p',
                    # 'author': 'xpath',
                },
                'attributes_relations': {
                    'date': '//div[contains(@class, "MaterialMeta--time")]',
                    # 'tag': 'xpath',
                    # 'region': 'xpath',
                },

                'related': '//div[@class="Related"]/ul/li/a/@href',
            },

            # Лента
            {
                'enabled': False,
                'name': 'Лента',
                'url': 'https://lenta.ru',
                'test_urls': ['https://lenta.ru/news/2017/04/17/extra_press/'],
                'yandex_news_id': 1047,

                'refresh_delay': 300,

                'detailed_page_re': '/news/[0-9]{4}/[0-9]{1,2}/[0-9]{1,2}/[_\w]+',

                'attributes_text': {
                    'title': '//h1[@class="b-topic__title"]',
                    'text': '//div[contains(@class, "b-text")]//p',
                    # 'author': 'xpath',
                },
                'attributes_relations': {
                    'date': '//div[@class="b-topic__info"]/time[@class="g-date"]',
                    # 'tag': 'xpath',
                    # 'region': 'xpath',
                },

                'related': '//section[contains(@class, "b-topic-addition")]/div[@class="item"]//a/@href',
            },

            # РБК
            {
                'enabled': False,
                'name': 'РБК',
                'url': 'http://www.rbc.ru',
                'test_urls': ['http://www.rbc.ru/technology_and_media/15/04/2017/58f0d19b9a7947d759c44d0f'],
                'yandex_news_id': 1027,

                'refresh_delay': 300,

                'detailed_page_re': '/[_\w]+/[0-9]{2}/[0-9]{2}/[0-9]{4}/[\w0-9]+',

                'attributes_text': {
                    'title': '//div[contains(@class, "article__header__title")]',
                    'text': '//div[contains(@class, "article__content")]//p',
                },
                'attributes_relations': {
                    'date': '//span[@class="article__header__date"]',
                },
            },

            # РИА
            {
                'enabled': True,
                'name': 'РИА',
                'url': 'http://ria.ru',
                'test_urls': ['https://ria.ru/incidents/20170416/1492361124.html'],
                'yandex_news_id': 1002,

                'refresh_delay': 300,

                'detailed_page_re': '/[_\w0-9]+/[0-9]{8}/[0-9]+\.html',

                'attributes_text': {
                    'title': '//h1[@class="b-article__title"]/span',
                    'text': '//div[contains(@class, "b-article__body")]/p',
                },
                'attributes_relations': {
                    'date': '//div[@class="b-article__info-date"]/span[2]',
                    'tag': '//ul[@class="b-article__tags-list"]/li/a/span',
                },

                'related': '//div[@class="b-inject__article-title"]/a/@href',
            },

            # Фонтанка
            {
                'enabled': True,
                'name': 'Фонтанка',
                'url': 'http://www.fontanka.ru',
                'test_urls': ['http://www.fontanka.ru/2017/04/16/064/'],
                'yandex_news_id': 1312,

                'refresh_delay': 300,

                'detailed_page_re': '/[0-9]{4}/[0-9]{2}/[0-9]{2}/[0-9]{3}/',

                'attributes_text': {
                    'title': '//h1[@class="article_title"]',
                    'text': '//div[@class="article_fulltext"]/p',
                },
                'attributes_relations': {
                    'date': '//div[contains(@class, "article_date")]',
                },

                'related': '//div[@class="center_article"]/div[@class="widget"]//div[@class="entry_title"]/a/@href',
            },

            # Свободная пресса
            {
                'enabled': True,
                'name': 'Свободная пресса',
                'url': 'http://svpressa.ru',
                'test_urls': ['http://svpressa.ru/world/news/170636/', 'http://svpressa.ru/politic/news/170638/'],
                'yandex_news_id': 9118,

                'refresh_delay': 300,

                'detailed_page_re': '/[-\w]+/[-\w]+/\d+/',

                'attributes_text': {
                    'title': '//h1[@class="b-text__title"]',
                    'text': '//div[contains(@class, "b-text__block_text")]/p',
                },
                'attributes_relations': {
                    'date': '//div[contains(@class, "b-text__date")]',
                },
            },

            # Эхо Петербурга
            {
                'enabled': True,
                'name': 'Эхо Петербурга',
                'url': 'http://echospb.ru',
                'test_urls': ['http://echospb.ru/2016/08/26/6-chelovek-pogibli-170-postradali-pri-vzrive-v-turcii/', 'http://echospb.ru/2017/04/18/novaya-mazda-cx-5-dlya-rf-dokumenti-uzhe-oformleni/'],
                'yandex_news_id': 3522,

                'refresh_delay': 300,

                'detailed_page_re': '/[0-9]{4}/[0-9]{2}/[0-9]{2}/[-\w]+/',

                'attributes_text': {
                    'title': '//h1[@class="post-title"]',
                    'text': '//div[contains(@class, "post-content")]//p',
                },
                'attributes_relations': {
                    'date': '//time[contains(@itemprop, "datePublished")]',
                },
            },

            # Взгляд
            {
                'enabled': True,
                'name': 'Взгляд',
                'url': 'http://www.vz.ru',
                'test_urls': ['http://www.vz.ru/news/2017/4/18/866721.html', 'http://www.vz.ru/politics/2013/10/8/653942.html'],
                'yandex_news_id': 2348,

                'refresh_delay': 300,

                'detailed_page_re': '/[-\w]+/[0-9]{4}/[0-9]{1,2}/[0-9]{1,2}/\d+\.html',

                'attributes_text': {
                    'title': '//h1',
                    'text': '//div[contains(@class, "text")]/p',
                },
                'attributes_relations': {
                    'date': '//p[contains(@class, "extra")]',
                },
            },

            # Московский Комсомолец в СПб
            {
                'enabled': False,
                'name': 'Московский Комсомолец в СПб',
                'url': 'http://spb.mk.ru',
                'test_urls': ['http://spb.mk.ru/articles/2011/12/16/653822-soli-na-dorogah-budet-menshe.html', 'http://spb.mk.ru/articles/2017/04/17/v-finale-kubka-gagarina-soshlis-ska-i-magnitka.html'],
                'yandex_news_id': 1429,

                'refresh_delay': 300,

                'detailed_page_re': '/[-\w]+/[0-9]{4}/[0-9]{1,2}/[0-9]{1,2}/[-\w]+\.html',

                'attributes_text': {
                    'title': '//h1',
                    'text': '//div[contains(@class, "content")]/p',
                },
                'attributes_relations': {
                    # todo чтобы из МК извлекать дату нужно писать костыль
                    # 'date': '//span[contains(@class, "date")]',
                },
            },

            # Лайф
            {
                'enabled': True,
                'name': 'Лайф',
                'url': 'https://life.ru',
                'test_urls': ['https://life.ru/t/новости/999284/papa_na_pokoie_bieniedikt_xvi_na_svoio_90-lietiie_pobaloval_siebia_pivom'],
                'yandex_news_id': 12694,

                'refresh_delay': 300,

                'detailed_page_re': '/\d+',     # Регулярка такая, т.к. на яндексе постят короткие ссылки

                'attributes_text': {
                    'title': '//h1',
                    'text': '//div[contains(@itemprop, "text")]/p',
                },
                'attributes_relations': {
                    'date': '//time[contains(@class, "published")]',
                },
            },
]
