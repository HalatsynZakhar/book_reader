import subprocess
import importlib
import os

# список необходимых модулей
required_modules = ['language_data', 'langcodes' ,'qtpy', 'pygame', 'requests', 'beautifulsoup4', 'nltk', 'mtranslate', 'googletrans==4.0.0-rc1' 'translators', 'gtts', 'python-vlc', 'PyQt5', 'lxml', 'chardet', 'unidecode']

# получаем список установленных модулей с помощью команды pip freeze
installed_modules = subprocess.check_output(['pip', 'freeze']).decode('utf-8').split('\n')

# проверяем каждый необходимый модуль на наличие в списке установленных модулей
for module in required_modules:
    if module not in installed_modules:
        # если модуль не установлен, устанавливаем его с помощью команды pip install
        subprocess.call(['pip', 'install', module])

# Пути к папкам для установки разных версий
path_3_1_0a0 = 'venv/Lib/site-packages/googletrans_3.1.0a0'
path_4_0_0rc1 = 'venv/Lib/site-packages/googletrans_4.0.0rc1'

# Создание папок, если они не существуют
os.makedirs(path_3_1_0a0, exist_ok=True)
os.makedirs(path_4_0_0rc1, exist_ok=True)


# Установка googletrans==3.1.0a0 в папку googletrans_3.1.0a0
subprocess.check_call(['pip', 'install', 'googletrans==3.1.0a0', '--target', path_3_1_0a0])

# Установка googletrans==4.0.0rc1 в папку googletrans_4.0.0rc1
subprocess.check_call(['pip', 'install', 'googletrans==4.0.0rc1', '--target', path_4_0_0rc1])