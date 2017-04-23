# coding=utf-8

sources = [
    # Фонтанка
    {
        'enabled': False,
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

    # Водитель_Петербурга
    {
        'enabled': True,
        'name': 'Водитель_Петербурга',
        'url': 'http://spbvoditel.ru',
        'test_urls': ['http://spbvoditel.ru/2017/04/16/003/'],
        'yandex_news_id': 9602,

        'refresh_delay': 600,

        'detailed_page_re': '/[0-9]{4}/[0-9]{2}/[0-9]{2}/[0-9]{3}/',

        'attributes_text': {
            'title': '//div[@class="text"]/h1',
            'text': '//div[@class="text"]/p',
        },
        'attributes_relations': {
            'date': '//div[@class="main-col"]/div[@class="title"]/text()[2]',
        },
    },

    # Главный_региональный
    {
        'enabled': True,
        'name': 'Главный_региональный',
        'url': 'http://sankt-peterburg.glavny.tv',
        'test_urls': ['https://sankt-peterburg.glavny.tv/news/59526'],
        'yandex_news_id': 254124829,

        'refresh_delay': 600,

        'detailed_page_re': '/\w+/[0-9]{5}',

        'attributes_text': {
            'title': '//h1[@id="page-title"]',
            'text': '//div[contains(@class, "pane-node-body")]//p',
        },
        'attributes_relations': {
            'date': '//div[@class="panel-pane pane-node-created no-title block"]/div',
        },
    },

    # Невские новости
    {
        'enabled': True,
        'name': 'Невские_новости',
        'url': 'https://nevnov.ru',
        'test_urls': ['https://nevnov.ru/483056-forvard-zenita-artem-dzyuba-chempionskaya-gonka-zakonchilas'],
        'yandex_news_id': 254106139,

        'refresh_delay': 600,

        'detailed_page_re': '/[0-9]{6}[-\w]+',

        'attributes_text': {
            'title': '//h1',
            'text': '//div[@class="text_content"]/p',
        },
        'attributes_relations': {
            'date': '//span[@class="date"]',
        },
    },

    # Neva today
    {
        'enabled': True,
        'name': 'Neva_today',
        'url': 'http://neva.today',
        'test_urls': ['http://neva.today/news/na-vasilevskom-ostrove-proizoshel-vzryv-postradal-podrostok-137440/'],
        'yandex_news_id': 254063050,

        'refresh_delay': 600,

        'detailed_page_re': '/news/[-\w\d]+/',

        'attributes_text': {
            'title': '//div[@class="full_article"]/h1',
            'text': '//div[@class="full_article"]/p',
        },
        'attributes_relations': {
            'date': '//div[@class="full_article"]//span[@class="time"]',
        },
    },
    # Бумага
    {
        'enabled': True,
        'name': 'Бумага',
        'url': 'http://paperpaper.ru',
        'test_urls': ['http://paperpaper.ru/papernews/2017/04/16/zenit-sprt/'],
        'yandex_news_id': 254067262,

        'refresh_delay': 600,

        'detailed_page_re': '/papernews/[0-9]{4}/[0-9]{2}/[0-9]{2}/',

        'attributes_text': {
            'title': '//h1[@class="r-text-title"]',
            'text': '//div[contains(@class, "r-text-content")]/div',
        },
        'attributes_relations': {
            'date': '//span[@class="r-date r-headline--right"]',
        },
    },
    # piter.tv
    {
        'enabled': True,
        'name': 'piter.tv',
        'url': 'http://piter.tv',
        'test_urls': ['http://piter.tv/event/Zhutkoe_video_iz_Moskvi_Mazeratti_na_skorosti_vrezalsya_v_stolb_i_zagorelsya/'],
        'yandex_news_id': 18694,

        'refresh_delay': 600,

        'detailed_page_re': '/event/[\w-]+',

        'attributes_text': {
            'title': '//div[@class="text-block"]/h1',
            'text': '//div[@id="articleBody"]/p',
        },
        'attributes_relations': {
            'date': '//div[@class="video-block-bottom-line"]/div[@class="date"]',
        },
    },
    # Петербургский_дневник
    {
        'enabled': True,
        'name': 'Петербургский_дневник',
        'url': 'http://www.spbdnevnik.ru',
        'test_urls': ['http://www.spbdnevnik.ru/news/2017-04-16/zenit--v-gostyakh-ustupil--spartaku/'],
        'yandex_news_id': 12556,

        'refresh_delay': 600,

        'detailed_page_re': '/news/[0-9]{4}-[0-9]{2}-[0-9]{2}',

        'attributes_text': {
            'title': '//h1/a[@class = "head"]',
            'text': '//div[@class="news-article"]/p',
        },
        'attributes_relations': {
            'date': '//div[@class="date-time"]/span[@class="date"]',
        },
    },
    # saint-petersburg.ru
    {
        'enabled': True,
        'name': 'saint_petersburg.ru',
        'url': 'http://saint-petersburg.ru/',
        'test_urls': ['http://saint-petersburg.ru/m/society/rubina/357723/'],
        'yandex_news_id': 1284,

        'refresh_delay': 600,

        'detailed_page_re': '/[-\w]+/[0-9]{6}/',

        'attributes_text': {
            'title': '//h1[@itemprop="name"]',
            'text': '//div[@itemprop="articleBody"]/span/p',
        },
        'attributes_relations': {
            'date': '//time[@itemprop="datePublished"]',
        },
    },
    # Росбалт
    {
        'enabled': True,
        'name': 'Росбалт',
        'url': 'http://www.rosbalt.ru',
        'test_urls': ['http://www.rosbalt.ru/piter/2017/04/16/1608030.html'],
        'yandex_news_id': 1063,

        'refresh_delay': 600,

        'detailed_page_re': '/piter/[0-9]{4}/[0-9]{2}/[0-9]{2}/',

        'attributes_text': {
            'title': '//article[@class="news"]/h1',
            'text': '//div[@class="newstext"]/p',
        },
        'attributes_relations': {
            'date': '//article[@class="news"]/div[@class="news-info"]',
        },
    },
]
