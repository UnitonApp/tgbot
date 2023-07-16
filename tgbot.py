import json
import requests

def send_message(chat_id, text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    data = {"chat_id": chat_id, "text": text}
    response = requests.post(url, json=data)
    return response.json()

def make_link(sum):
    curtime = int(time.time())
    str2ins = f"INSERT INTO `paylinks` (`chatid`,`times`,`status`,`sum`) VALUES ('{chat_id}','{curtime}','0','{sum}')"
    mysqli_query(link, str2ins)
    last_id = mysqli_insert_id(link)
    secret = roskassa_secretkey
    data = {
        "shop_id": roskassa_publickey,
        "amount": sum,
        "currency": "RUB",
        "order_id": chat_id
    }
    data_str = '&'.join([f"{k}={v}" for k, v in data.items()])
    sign = hashlib.md5((data_str + secret).encode()).hexdigest()
    formpage = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Payment Form</title>
        </head>
        <body>
            <div align="center">
                <br><br>
                You are paying: <br>
                <span style="font-size: 24px; font-weight: bold;">{sum} RUB</span><br><br>
                <form action="https://tegro.money/pay/" method="post">
                    <input type="hidden" name="shop_id" value="{roskassa_publickey}">
                    <input type="hidden" name="amount" value="{sum}">
                    <input type="hidden" name="order_id" value="{chat_id}">
                    <input type="hidden" name="lang" value="ru">
                    <input type="hidden" name="currency" value="RUB">
                    <input type="hidden" name="sign" value="{sign}">
                    <input type="submit" value="Pay" style="width: 200px; padding: 15px;">
                </form>
            </div>
        </body>
        </html>
    """
    filename = f"payform/{chat_id}_{time.time()}.php"
    with open(filename, "w+") as file:
        file.write(formpage)
    return f"https://tegro.money/pay/?{data_str}&sign={sign}"

def send(chat_id, message, keyboard=None):
    data = {"chat_id": chat_id, "text": message}
    if keyboard == "DEL":
        data["reply_markup"] = {"remove_keyboard": True}
    elif keyboard:
        data["reply_markup"] = {"keyboard": keyboard, "resize_keyboard": True}
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    response = requests.post(url, json=data)
    return response.json()

def build_service_list(num):
    prefix = ""
    if num == 1:
        prefix = "inst-"
    elif num == 2:
        prefix = "vk-"
    elif num == 3:
        prefix = "yt-"
    # и так далее для остальных услуг
    str2select = f"SELECT * FROM `smoservices` WHERE `code` LIKE '%{prefix}%'"
    result = mysqli_query(link, str2select)
    c = 0
    keyboard = []
    while row = @mysqli_fetch_object(result):
        keyboard.append([row.name])
        c += 1
    keyboard.append(["Назад"])
    send(chat_id, "Выберите сервис:", keyboard)

def order_service(num):
    str2select = f"SELECT * FROM `smoservices` WHERE `id`='{num}'"
    result = mysqli_query(link, str2select)
    row = @mysqli_fetch_object(result)
    curtime = int(time.time())
    str2ins = f"INSERT INTO `temp_sess` (`chatid`,`serviceid`,`times`,`otipe`) VALUES ('{chat_id}','{num}','{curtime}','order')"
    mysqli_query(link, str2ins)
    send(chat_id, f"Заказ услуги '{row.name}'\nЦена - {row.price} RUB за одну единицу (Подписчик, лайк, репост)\nВведите количество для заказа от {row.min} до {row.max}:")

def delayed_start():
    str2select = f"SELECT * FROM `delayed_posts` WHERE `chatid`='{chat_id}'"
    result33 = mysqli_query(link, str2select)
    if(mysqli_num_rows(result33) == 0):
        sendtime = int(time.time()) + 86400 * 14
        str2ins = f"INSERT INTO `delayed_posts` (`chatid`,`times`,`post_id`) VALUES ('{chat_id}','{sendtime}','0')"
        mysqli_query(link, str2ins)
        send(chat_id, "Ваш аккаунт активирован!")

def execute_command(update):
    message = update["message"]
    chat_id = message["chat"]["id"]
    text = message.get("text")
    if text == "/start":
        delayed_start()
        send(chat_id, "Welcome!", [["Создать новый заказ"], ["Мои заказы", "Мой баланс"], ["Заработать", "Поддержка"], ["FAQ"]])
    elif text == "Создать новый заказ" or text == "/create_order":
        build_service_list(0)
    elif text == "Мои заказы" or text == "/my_orders":
        str2select = f"SELECT * FROM `orders` WHERE `chatid`='{chat_id}' ORDER BY `times` DESC"
        result = mysqli_query(link, str2select)
        c = 0
        while row = @mysqli_fetch_object(result):
            c += 1
            send(chat_id, f"Заказ №{c}\nДата: {datetime.fromtimestamp(int(row.times)).strftime('%Y-%m-%d %H:%M:%S')}\n{row.services}\nСтоимость: {row.totalprice} RUB\nСтатус: {row.status}\nСсылка: {row.link}")
        if c == 0:
            send(chat_id, "У вас нет заказов.")
    elif text == "Мой баланс" or text == "/my_balance":
        str2select = f"SELECT * FROM `users` WHERE `chatid`='{chat_id}'"
        result = mysqli_query(link, str2select)
        row = @mysqli_fetch_object(result)
        send(chat_id, f"Ваш баланс: {row.balance} RUB")
    elif text == "Заработать" or text == "/earn":
        send(chat_id, "Реферальная программа:\n\nПриглашайте друзей по вашей реферальной ссылке и получайте 10% от суммы их пополнений!\n\nВаша реферальная ссылка:\nhttps://t.me/{bot_name}?start={chat_id}")
    elif text == "Поддержка" or text == "/support":
        send(chat_id, "Если у вас возникли вопросы или проблемы, свяжитесь с нашей службой поддержки:\n\nEmail: support@example.com\nТелефон: +1234567890")
    elif text == "FAQ" or text == "/faq":
        send(chat_id, "Часто задаваемые вопросы:\n\nQ: Как создать заказ?\nA: Чтобы создать новый заказ, выберите 'Создать новый заказ' в главном меню и следуйте инструкциям.\n\nQ: Как проверить статус заказа?\nA: Вы можете проверить статус своих заказов, выбрав 'Мои заказы' в главном меню.\n\nQ: Как связаться с поддержкой?\nA: Для связи с нашей службой поддержки, выберите 'Поддержка' в главном меню.")
    elif text.isdigit():
        str2select = f"SELECT * FROM `temp_sess` WHERE `chatid`='{chat_id}' AND `otipe`='order'"
        result = mysqli_query(link, str2select)
        if(mysqli_num_rows(result) == 0):
            build_service_list(int(text))
        else:
            row = @mysqli_fetch_object(result)
            if(int(text) < row.min or int(text) > row.max):
                send(chat_id, f"Введите количество для заказа от {row.min} до {row.max}:")
            else:
                str2select = f"SELECT * FROM `smoservices` WHERE `id`='{row.serviceid}'"
                result = mysqli_query(link, str2select)
                row = @mysqli_fetch_object(result)
                cost = row.price * int(text)
                if(row.min > 0):
                    cost -= row.min
                str2update = f"UPDATE `temp_sess` SET `otipe`='order {text}' WHERE `chatid`='{chat_id}' AND `otipe`='order'"
                mysqli_query(link, str2update)
                str2ins = f"INSERT INTO `orders` (`chatid`,`times`,`services`,`totalprice`,`status`,`link`) VALUES ('{chat_id}','{int(time.time())}','{row.name} - {text}','{cost}','Ожидает оплаты','0')"
                mysqli_query(link, str2ins)
                str2select = f"SELECT * FROM `users` WHERE `chatid`='{chat_id}'"
                result = mysqli_query(link, str2select)
                row = @mysqli_fetch_object(result)
                if(row.balance >= cost):
                    str2update = f"UPDATE `users` SET `balance`=`balance`-'{cost}' WHERE `chatid`='{chat_id}'"
                    mysqli_query(link, str2update)
                    str2select = f"SELECT * FROM `orders` WHERE `chatid`='{chat_id}' ORDER BY `times` DESC"
                    result = mysqli_query(link, str2select)
                    row = @mysqli_fetch_object(result)
                    str2update = f"UPDATE `orders` SET `status`='Выполняется' WHERE `id`='{row.id}'"
                    mysqli_query(link, str2update)
                    send(chat_id, f"Заказ #{row.id}\nУслуга: {row.services}\nСтоимость: {row.totalprice} RUB\n\nОплатите заказ по ссылке:\n{make_link(row.totalprice)}")
                else:
                    send(chat_id, "Недостаточно средств на балансе. Пополните баланс для продолжения.")
    else:
        send(chat_id, "Команда не найдена. Пожалуйста, используйте меню для взаимодействия с ботом.")

# Пример использования
TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
bot_name = "YOUR_BOT_USERNAME"

# Получение обновлений от Telegram API (примерно)
updates = requests.get(f"https://api.telegram.org/bot{TOKEN}/getUpdates").json()

# Обработка каждого обновления
for update in updates["result"]:
    execute_command(update)
