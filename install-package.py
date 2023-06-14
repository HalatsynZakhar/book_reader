import subprocess

# список необходимых модулей
required_modules = ['language_data', 'langcodes' ,'qtpy', 'pygame', 'requests', 'beautifulsoup4', 'nltk', 'googletrans==3.1.0a0', 'gtts', 'python-vlc', 'PyQt5', 'lxml']

# получаем список установленных модулей с помощью команды pip freeze
installed_modules = subprocess.check_output(['pip', 'freeze']).decode('utf-8').split('\n')

# проверяем каждый необходимый модуль на наличие в списке установленных модулей
for module in required_modules:
    if module not in installed_modules:
        # если модуль не установлен, устанавливаем его с помощью команды pip install
        subprocess.call(['pip', 'install', module])