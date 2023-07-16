import requests
import json

params = {
    "user_id": user_id,
    "api_key": api_key,
    "action": 'services'
}

# sending POST request
response = requests.post('https://smoservice.media/api/', data=params)

if response.text != '':
    # Assuming you have established a database connection
    cursor = link.cursor()
    cursor.execute("TRUNCATE TABLE `smoservices`")

    data = json.loads(response.text)
    for item in data['data']:
        columns = ""
        values = ""
        for key, value in item.items():
            columns += "`" + key + "`,"
            values += "'" + value + "',"

        columns = columns[:-1]
        values = values[:-1]

        str2ins = f"INSERT INTO `smoservices` ({columns}) VALUES ({values})"
        cursor.execute(str2ins)

    link.commit()
    cursor.close()
