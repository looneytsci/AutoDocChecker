[AutoDocChecker]

* Getting Started

[User]
Вызовите команду AutoDocChecker.exe в корне репозитория.
Используйте аргументы для кастомизации прогона:

- *file_name*.json - установить input файл
- --silent - запустить программу без открытия браузера.

Программа работет с браузером Google Chrome (112+).

[Developer]
Для начала работы нужно установить [Python3](https://www.python.org/downloads/release/python-3132/) актуальной версии, а так же зависимости:
 - selenium
 - PIL
 - easyocr
 - opencv-python

Для установки зависимостей просто вызовите команду 'make install_dependencies' из рута репозитория.