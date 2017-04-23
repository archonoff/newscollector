# coding=utf-8

from py2neo import Graph
from py2neo.ogm import GraphObject
from json import dumps

from newscollector.generic_functions import normalizer
from newscollector.settings import *
from newscollector.my_exceptions import ConfigurationError, DBError
from newscollector.models import Source, News, Date, Tag, Region


graph = Graph(host=GRAPH_HOST, password=GRAPH_PASS)


def get_or_create(model, identifier):
    """
    Возвращает модель с заданным идентификатором, либо создает ее
    :type model: GraphObject
    :type identifier: str
    :rtype: GraphObject
    """
    tx = graph.begin()
    node = model.select(tx, identifier).first()
    if node is not None:
        tx.commit()
        return node
    else:
        # Добавление новой ноды
        node = model(tx)
        setattr(node, model.__primarykey__, identifier)
        # node.save()
        tx.create(node)
        tx.commit()
        return node


def get_news_from_db(config, url):
    """
    Функция проверяет, не содержится ли новость уже в БД
    """
    source_name = config.get('name')
    news = News.select(graph, url).first()
    if news is None:
        # Если новость по ссылке не нашлась
        return None
    else:
        return news
        # todo тут необходимо добавить проверку и на источник тоже
        if news.FROM.get(Source, 'name') == source_name:
            # Если новость все же нашлась, и имя источника совпадает с данным
            return news
        else:
            # Иначе просто случайное совпадение ссылки
            return None


def is_source_in_db(config):
    """
    Функция проверяет, находится ли данный источник в БД
    :rtype: bool
    """
    name = config.get('name')
    if Source.select(graph, name).first() is None:
        return False
    else:
        return True


def add_source_if_missed(config):
    """
    Добавляет источник, если его нет в базе, по данным из конфига
    """
    def is_source_in_db2():
        """
        Функция проверяет, находится ли данный источник в БД
        :rtype: bool
        """
        name = config.get('name')
        if Source.select(tx, name).first() is None:
            return False
        else:
            return True
    tx = graph.begin()
    if is_source_in_db2():
        tx.commit()
        return
    # Добавление
    name = config.get('name')
    url = config.get('url')
    if not name or not url:
        tx.commit()
        raise ConfigurationError('Fields "name" or "url" are not found in config')
    source = Source(tx)
    source.name = name
    source.url = url
    tx.create(source)
    tx.commit()


def add_relation(to_news, from_news):
    """
    Добавляет связь между двумя существующими новостями
    :type to_news: News
    :type from_news: News
    """
    to_news.relations.add(from_news)
    graph.push(to_news)


def add_news(config, url, grab, related_from_url, region=None):
    """
    Добавляет новость с аттрибутами
    """
    source_name = config.get('name')
    attributes_text = config.get('attributes_text')
    attributes_relations = config.get('attributes_relations')

    news = News(graph)
    news.news_url = url
    news.FROM.add(get_or_create(Source, source_name))

    # Аттрибуты, которых сохраняются в ноде новости
    data_text = {}
    for attr_name, xpath in attributes_text.items():
        attribute = '\n'.join(grab.doc.select(xpath).text_list())
        data_text[attr_name] = attribute
    news.attributes = dumps(data_text)

    # Аттрибуты, которые связаны с нодой новости отношениями
    for attr_name, xpath in attributes_relations.items():
        attributes = grab.doc.select(xpath).text_list()
        for attribute in attributes:
            attribute = normalizer(attribute, attr_name)        # Нормализация значения аттрибута
            if attr_name == 'date':
                news.POSTED.add(get_or_create(Date, attribute))
            elif attr_name == 'tag':
                news.TAGGED.add(get_or_create(Tag, attribute))
            elif attr_name == 'region':
                news.WHERE.add(get_or_create(Region, attribute))
            else:
                # Аттрибут не предусмотрен моделью данных
                raise DBError('Attribute "{}" is not supported by database'.format(attr_name))

    # Добавляем регион, переданный извне при загрузке новости
    if region is not None:
        # todo баг: регион добавляется 2 раза
        news.WHERE.add(get_or_create(Region, region))

    if related_from_url is not None:
        news.relations.add(get_news_from_db(config, related_from_url))

    news.save()


def set_related_news(relations):
    l = len(relations)
    for i, (from_node_url, to_node_urls) in enumerate(relations):
        p = i / float(l)
        if i % 1000 == 0:
            print('Processed {:.2%} nodes'.format(p))
        from_node = News.select(graph, from_node_url).first()
        if from_node:
            for to_node_url in to_node_urls:
                to_node = News.select(graph, to_node_url).first()
                if to_node:
                    from_node.RELATED.add(to_node)
                    graph.push(from_node)


# Установка отношений при загрузки из пиклов
# from pickle import load
# with open('related.pkl', 'rb') as f:
#     relations = load(f)
#     set_related_news(relations)

# for a in Source.select(g, 'Meduza').first().news:
#     print a.title
#
# add_source(name='Meduza', url='https://meduza.io/')
