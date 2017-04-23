from unittest import TestCase
import re
from grab import Grab
import dateparser

from ..sources_config import sources as sources_main
from ..sources_dtp_config import sources as sources_dtp


def test_assertIsNotNone(val, msg):
    def test(self):
        self.assertIsNotNone(val, msg)
    return test


def test_assertEqual(val1, val2, msg):
    def test(self):
        self.assertEqual(val1, val2, msg)
    return test


def test_assertGreater(val1, val2, msg):
    def test(self):
        self.assertGreater(val1, val2, msg)
    return test


class ConfigTest(TestCase):
    """Тест конфигураций. Тестовые функции добавляются динамически"""


# Генератор тестов для каждого источника
for sources in (sources_main, sources_dtp):
    for source in sources:
        re_expr = source.get('detailed_page_re')
        attributes_text = source.get('attributes_text')
        attributes_relations = source.get('attributes_relations')
        for test_url in source.get('test_urls'):
            # Тест регулярного выражения строки распознавания урла
            search_res = re.search(re_expr, test_url)
            test_name = 'test_regexp_{}'.format(source.get('name'))
            test = test_assertIsNotNone(search_res, test_url)
            setattr(ConfigTest, test_name, test)

            # Тест нахождения контента на страницах
            grab = Grab(timeout=90, connect_timeout=30)
            grab.go('{}'.format(test_url))

            # Тест кода ответа
            test_name = 'test_resp_code_{}'.format(source.get('name'))
            test = test_assertEqual(grab.response.code, 200, test_url)
            setattr(ConfigTest, test_name, test)

            for attr_name, xpath in attributes_text.items():
                attributes = grab.doc.select(xpath).text_list()
                test_name = 'test_attribute_{}_for_{}'.format(attr_name, source.get('name'))
                test = test_assertGreater(len(attributes), 0, test_url)
                setattr(ConfigTest, test_name, test)

            for attr_name, xpath in attributes_relations.items():
                attributes = grab.doc.select(xpath).text_list()
                test_name = 'test_attribute_{}_for_{}'.format(attr_name, source.get('name'))
                test = test_assertGreater(len(attributes), 0, test_url)
                setattr(ConfigTest, test_name, test)

                # Проверка обработки извлеченной даты
                if attr_name == 'date' and attributes:
                    date_str = attributes[0]
                    test_name = 'test_date_format_for_{}'.format(source.get('name'))
                    test = test_assertIsNotNone(dateparser.parse(date_str, languages=['ru']), test_url)
                    setattr(ConfigTest, test_name, test)

            # todo добавить проверку xpath для отношений
