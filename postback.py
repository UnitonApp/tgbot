import requests
import json

def sendit(response, restype):
    url = f"https://api.telegram.org/bot{TOKEN}/{restype}"
    r = requests.post(url, json=response)
    r.close()

def send(id, message, keyboard):
    # Удаление клавиатуры
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

link = mysqli.connect(hostName, userName, password, databaseName)

tofile = ''
for key, value in request.form.items():
    globals()[key] = value.strip()

    tofile += f"{key}:{value}\n"

with open("response.txt", "w+") as file:
    file.write(tofile)

data = request.form.to_dict(flat=False)
data = {k: v[0] for k, v in data.items()}
data_sorted = dict(sorted(data.items()))
str_data = "&".join([f"{k}={v}" for k, v in data_sorted.items()])
sign2 = md5((str_data + roskassa_secretkey).encode()).hexdigest()

tofile = f"""
===========
{str_data}
sign from roskassa: {sign}
sign from script: {sign2}
"""

with open("response.txt", "a+") as file:
    file.write(tofile)

#if sign != sign2:
#    exit()

orderstarted = ''

# check for pending order
str2select = f"SELECT * FROM `temp_sess` WHERE `chatid`='{order_id}' AND (`otipe`='order' AND `waitpayment`='1') ORDER BY `rowid` DESC LIMIT 1"
result = link.query(str2select)
if result.num_rows != 0:
    row = result.fetch_object()

    str3select = f"SELECT * FROM `smoservices` WHERE `id`='{row.serviceid}'"
    result3 = link.query(str3select)
    row3 = result3.fetch_object()
    ordersum = row.volume * row3.price
    curtime = time()

    str2ins = f"INSERT INTO `orders` (`chatid`,`serviceid`,`volume`,`sum`,`times`) VALUES ('{order_id}','{row.serviceid}','{row.volume}','{ordersum}','{curtime}')"
    link.query(str2ins)
    orderno = link.insert_id

    amount -= ordersum

    # SEND ORDER TO API smoservice
    params = {
        "user_id": user_id,
        "api_key": api_key,
        "action": 'create_order',
        "service_id": row.serviceid,
        "count": row.volume,
        "url": row.page
    }

    response = requests.post('https://smoservice.media/api/', data=params)
    smodata = json.loads(response.text)
    response.close()

    if smodata['type'] == 'success':
        str3upd = f"UPDATE `orders` SET `smoorderid`='{smodata['data']['order_id']}' WHERE `rowid`='{orderno}'"
        link.query(str3upd)

        # Referrals
        str5select = f"SELECT * FROM `users` WHERE `chatid`='{order_id}'"
        result5 = link.query(str5select)
        row5 = result5.fetch_object()

        if row5.ref != 0:
            earn = (ordersum / 100) * refpercent
            str4upd = f"UPDATE `balance` SET `sum`=`sum`+{earn} WHERE `chatid`='{row5.ref}'"
            link.query(str4upd)
####################### 2022 #####################
            str10upd = f"UPDATE `users` SET `refbalance`=`refbalance`+{earn} WHERE `chatid`='{row5.ref}'"
            link.query(str10upd)
####################### 2022 #####################

        orderstarted = '\nЗаказ отправлен в обработку'

    str2del = f"DELETE FROM `temp_sess` WHERE `rowid` = '{row.rowid}'"
    link.query(str2del)

# check for pending order

amount = round(amount, 2)

str2select = f"SELECT * FROM `balance` WHERE `chatid`='{order_id}'"
result = link.query(str2select)
if result.num_rows == 0:
    str2ins = f"INSERT INTO `balance` (`chatid`,`sum`) VALUES ('{order_id}','{amount}')"
    link.query(str2ins)
else:
    str2ins = f"UPDATE `balance` SET `sum`=`sum`+{amount} WHERE `chatid`='{order_id}'"
    link.query(str2ins)

response = {
    'chat_id': order_id,
    'text': f'Успешно пополнен баланс на {amount} рублей{orderstarted}'
}
sendit(response, 'sendMessage')

link.close()
