# coding=utf-8

import dateparser


def normalizer(attribute, attr_name):
    """
    Функция для нормализации данных. Например, приведения даты в единый формат
    :type attribute: str
    :type attr_name: str
    :rtype: str
    """
    if attr_name == 'date':
        date = dateparser.parse(attribute, languages=['ru']).date()
        return str(date)
    elif attr_name == 'tag':
        return attribute.strip('#')
    return attribute
