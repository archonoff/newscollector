# coding=utf-8

# Данные для доступа к Neo4j
GRAPH_HOST = 'localhost'
GRAPH_PASS = '1111'

# Настройки обработки рекурсивных и связанных ссылок
# Рекомендуется держать их выключенными! Т.к. с включенной данной настройкой, количество ссылок на обработку в очереди растет очень быстро
PROCESS_RECURSIVE_LINKS = False
PROCESS_RELATED_LINKS = False

# Данные для доступа к Celery
CELERY_BACKEND = 'rpc://guest@localhost//'
CELERY_BROKER = 'pyamqp://guest@localhost//'

try:
    from .local_settings import *
except:
    pass
