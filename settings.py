import configparser

conf = configparser.ConfigParser()
conf.read('settings.ini')

db_name = conf['db']['name']
db_driver = conf['db']['driver']

web_port = int(conf['web']['port'])
