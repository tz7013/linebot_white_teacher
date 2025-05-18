import requests
from bs4 import BeautifulSoup
import os

def get_zodiac_sign(msg):
    if msg.isdigit():
        month = int(msg[0:2])
        day = int(msg[2:])
        if (month == 1 and day >= 20) or (month == 2 and day <= 18):
            return "Aquarius", 10
        elif (month == 2 and day >= 19) or (month == 3 and day <= 20):
            return "Pisces", 11
        elif (month == 3 and day >= 21) or (month == 4 and day <= 19):
            return "Aries", 12
        elif (month == 4 and day >= 20) or (month == 5 and day <= 20):
            return "Taurus", 1
        elif (month == 5 and day >= 21) or (month == 6 and day <= 20):
            return "Gemini", 2
        elif (month == 6 and day >= 21) or (month == 7 and day <= 22):
            return "Cancer", 3
        elif (month == 7 and day >= 23) or (month == 8 and day <= 22):
            return "Leo", 4
        elif (month == 8 and day >= 23) or (month == 9 and day <= 22):
            return "Virgo", 5
        elif (month == 9 and day >= 23) or (month == 10 and day <= 22):
            return "Libra", 6
        elif (month == 10 and day >= 23) or (month == 11 and day <= 21):
            return "Scorpio", 7
        elif (month == 11 and day >= 22) or (month == 12 and day <= 21):
            return "Sagittarius", 8
        elif (month == 12 and day >= 22) or (month == 1 and day <= 19):
            return "Capricorn", 9
        else:
            return "Invalid Date"
        
    else:
        zodiac = ("金牛", "雙子", "巨蟹", "獅子", "處女", "天秤", "天蠍", "射手", "摩羯", "水瓶", "雙魚", "白羊")
        for i in range(len(zodiac)):
            if msg[:2] == zodiac[i]:
                return zodiac[i], i+1


def horoscope(zodiac_num):
    horoscope_html = f"horoscope_file/{zodiac_num}.html"
    
    if os.path.isfile(horoscope_html):
        print("檔案存在。")

    else: 
        url = f"https://astro.click108.com.tw/daily_{zodiac_num}.php?iAstro={zodiac_num}"
        response = (requests.get(url))

        with open (horoscope_html, 'w', encoding = 'utf-8') as file:
            file.write(response.text)

    with open (horoscope_html, 'r', encoding = 'utf-8') as file:
        data = file.read()

        soup = BeautifulSoup(data, 'html.parser')
        # print(soup.prettify())

        data = soup.find_all(class_="TODAY_CONTENT")
        horoscope = data[0].text.strip()
    
    return horoscope


def get_local_weather(local):
    # 將"台"改為"臺""
    if local.startswith("台"):
        local = "臺" + local[1:]

    # API 授權碼與 URL
    API_KEY = "CWA-39A4E043-14A1-4D72-B097-B2D1F2C9A675"
    API_URL = f"https://opendata.cwa.gov.tw/api/v1/rest/datastore/F-C0032-001?Authorization={API_KEY}"

    # 發送 GET 請求
    response = requests.get(API_URL)
    data = response.json()

    # 取得地區的天氣資料
    location = next(loc for loc in data["records"]["location"] if local in loc["locationName"])
    weather_elements = {el["elementName"]: el["time"] for el in location["weatherElement"]}
    locationName = location['locationName']

    # 整理摘要
    summary = []
    for i in range(len(weather_elements["Wx"])):
        start = weather_elements["Wx"][i]["startTime"][:-3].replace("-", "/")
        end = weather_elements["Wx"][i]["endTime"][:-3].replace("-", "/")
        wx = weather_elements["Wx"][i]["parameter"]["parameterName"]
        pop = weather_elements["PoP"][i]["parameter"]["parameterName"] + "%"
        min_t = weather_elements["MinT"][i]["parameter"]["parameterName"] + "°C"
        max_t = weather_elements["MaxT"][i]["parameter"]["parameterName"] + "°C"
        ci = weather_elements["CI"][i]["parameter"]["parameterName"]

        summary.append(f'{start}~{end}: 氣溫{min_t}~{max_t}, 降雨機率{pop}, {wx}, {ci}')


    # 輸出結果
    msg = f"🌤 {locationName}36小時天氣"
    for block in summary:
        msg = msg + '\n\n' + "> " + block
    
    return msg

if __name__ == "__main__":
    # msg = "1111"
    # print(get_zodiac_sign(msg))
    print(get_local_weather("台北"))



