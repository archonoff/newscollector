# broker_url = 'pyamqp://guest@localhost//'
# result_backend = 'rpc://guest@localhost//'
broker_url = 'pyamqp://guest@192.168.1.108//'
result_backend = 'rpc://guest@192.168.1.108//'

# List of modules to import when the Celery worker starts.
imports = ('newscollector.newscollector_worker',)

# task_annotations = {'tasks.add': {'rate_limit': '10/s'}}

# CELERY_ACCEPT_CONTENT = ['pickle']
task_serializer = 'pickle'
result_serializer = 'pickle'
# accept_content = {'pickle'}
