import requests


def get_course():
    url = 'https://www.floatrates.com/daily/usd.json'
    response = requests.get(url=url)
    if response.status_code == 200:
        json_data = response.json()
        rub_data = json_data.get("rub")
        if rub_data:
            course = {
                "Currency Code": rub_data["code"],
                "Name": rub_data["name"],
                "Exchange Rate": rub_data["rate"],
                "Date": rub_data["date"],
                "Inverse Rate": rub_data["inverseRate"],
            }
            return course
