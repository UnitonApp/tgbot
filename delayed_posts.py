import requests
import json
import time

link = mysqli.connect(hostName, userName, password, databaseName)
curtime = time.time()

# Select all positions to send
str2select = f"SELECT * FROM `delayed_posts` WHERE `sendtime` <= {curtime}"
result = link.query(str2select)
while row = result.fetch_object():
    if row.stop == 1:
        continue

    response = {
        'chat_id': row.chatid,
        'text': "*Не дай боту заскучать* " + '😫' + "\n\nВерный спутник SMM-продвижения по прежнему здесь. Без обеда и выходных, он принимает заказы. Подписчики, Лайки и просмотры!\n\n1. Напишите команду /start\n\n2. Выберите услугу\n\n3. Укажите параметры\n\n*Раз, два, три - и ваш заказ на получение лайков, просмотров и подписчиков запущен*" + '😍',
        'parse_mode': 'Markdown'
    }
    sendit(response, 'sendMessage')

    # Update the record
    sendtime = curtime + 86400*14
    str2upd = f"UPDATE `delayed_posts` SET `sendtime` = {sendtime} WHERE `rowid` = {row.rowid}"
    link.query(str2upd)

# end WHILE MySQL
link.close()

exit('ok')  # Обязательно возвращаем "ok", чтобы телеграмм не подумал, что запрос не дошёл

def sendit(response, restype):
    url = f"https://api.telegram.org/bot{TOKEN}/{restype}"
    r = requests.post(url, json=response)
    r.close()

def send(id, message, keyboard):
    # Удаление клавы
    if keyboard == "DEL":
        keyboard = {
            'remove_keyboard': True
        }
    if keyboard:
        # Отправка клавиатуры
        encodedMarkup = json.dumps(keyboard)

        data = {
            'chat_id': id,
            'text': message,
            'reply_markup': encodedMarkup
        }
    else:
        # Отправка сообщения
        data = {
            'chat_id': id,
            'text': message
        }

    out = sendit(data, 'sendMessage')
    return out
