from BracketHub.settings.base import *

DEBUG = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'prod.sqlite3'),
    }
    # 'default': {
    #     'ENGINE': 'django.db.backends.mysql',
    #     'NAME': 'tjmcdonough45$bracketracker',
    #     'USER': 'tjmcdonough45',
    #     'PASSWORD': 'hungryHungryhippos69',
    #     'HOST': 'tjmcdonough45.mysql.pythonanywhere-services.coms',
    # }
}
