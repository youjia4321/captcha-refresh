# captcha-refresh
django中的captcha模块及前端ajax刷新验证码

先安装captcha模块  pip install django-simple-captcha

将模块注册到settings的app中

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'robot',
    'captcha',
]
