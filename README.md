
# Приложение Tbot

Telegram-бот, для добавления и просмотра списка задач.



## Структура работы:

- Добавялет задачу с помощью команды /add
- Отменяет добавление задачи с помощью инлай-клавиатуры /cancel
- Показывает список задач с помощью команды /list
- Удаляет задачу с помощью команды /delete


## Технологический стек:

- Python 3
- aiogram
- asyncio
- logging


## Установка приложения:

Клонировать репозиторий:

```bash
 git clone git@github.com:ralinsg/tbot.git

```
Перейти в склонированный репозиторий:
```bash
 cd tbot
```
Cоздать виртуальное окружение:
```bash
py -3.7 -m venv venv
```
Активировать виртуальное окружение:
```bash
 source venv/bin/activate
```
Установить зависимости из файла requirements.txt:
```bash
 pip install -r requirements.txt
```
Создать файл .env со следующими данными:
```bash
BOT_TOKEN = <Токен telegramm-бота>
WEBHOOK_HOST = <IP-адрес сервера>
PORT = <Порт>

```

## Запуск проекта:

```bash
 python bot_telegram.py
```


## Автор

- Ралин Сергей [@ralinsg](https://github.com/ralinsg)
