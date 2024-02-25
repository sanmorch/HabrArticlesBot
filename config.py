from configparser import ConfigParser


def config(filename='database.ini', section='postgresql'):
    parser = ConfigParser()
    parser.read(filename)
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception('Section {0} is not found in the {1} file.'.format(section, filename))
    return db


# for bot token
TOKEN_API = "6826629475:AAHOoF18iJqGRG1sSqwKWsnpWKPHb9TF5Uk"
HELP_COMMAND = '''
/help - список команд 
/start - начать работу с ботом 
/another_comand
'''

# URLs
URL_BASIC = "https://habr.com"
URL_TOPICS = "https://habr.com/ru/hubs/page"
URL_FLOW = "https://habr.com/ru/flows/"  # https://habr.com/ru/flows/ + FLOW_NAME + "/articles

# constants
FLOWS = {'Разработка': 'develop',
         'Администрирование': 'admin',
         'Дизайн': 'design',
         'Менеджмент': 'management',
         'Маркетинг': 'marketing',
         'Научпоп': 'popsci'}
