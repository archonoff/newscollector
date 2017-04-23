# coding=utf-8

"""Модель данных хранения новостей для графовой БД"""

from py2neo.ogm import GraphObject, Property, RelatedTo, RelatedFrom


class SaverMixin:
    def __init__(self, graph):
        self.graph = graph

    def save(self):
        self.graph.push(self)


class News(SaverMixin, GraphObject):
    __primarykey__ = 'news_url'

    news_url = Property()
    attributes = Property()     # Для json сериализации аттрибутов новости (текст, название, прочие)

    RELATED = RelatedTo('News')        # Главное отношение графа
    FROM = RelatedTo('Source')
    POSTED = RelatedTo('Date')
    TAGGED = RelatedTo('Tag')
    WHERE = RelatedTo('Region')
    CONTAINS = RelatedTo('Entity')

    relations = RelatedFrom('News', 'RELATED')


class Source(SaverMixin, GraphObject):
    __primarykey__ = 'name'

    name = Property()
    url = Property()
    config_file = Property()

    HAS = RelatedTo('Attribute')
    news = RelatedFrom('News', 'FROM')


class Tag(SaverMixin, GraphObject):
    __primarykey__ = 'name'

    name = Property()

    news = RelatedFrom('News', 'TAGGED')


class Region(SaverMixin, GraphObject):
    __primarykey__ = 'name'

    name = Property()

    news = RelatedFrom('News', 'WHERE')


class Date(SaverMixin, GraphObject):
    __primarykey__ = 'date'

    date = Property()

    news = RelatedFrom('News', 'POSTED')


class Entity(SaverMixin, GraphObject):
    __primarykey__ = 'value'

    value = Property()
    type = Property()

    news = RelatedFrom('News', 'CONTAINS')


class Attribute(SaverMixin, GraphObject):
    __primarykey__ = 'name'

    name = Property()

    sources = RelatedFrom('Source', 'HAS')
