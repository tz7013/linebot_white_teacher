import requests

# API 授權碼與 URL
API_KEY = "CWA-39A4E043-14A1-4D72-B097-B2D1F2C9A675"
API_URL = f"https://opendata.cwa.gov.tw/api/v1/rest/datastore/F-C0032-001?Authorization={API_KEY}"

# 發送 GET 請求
response = requests.get(API_URL)
data = response.json()


# 取得地區的天氣資料
location = next(loc for loc in data["records"]["location"] if loc["locationName"] == "新北市")
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
msg = f"🌤 新北市36小時天氣"
for block in summary:
    msg = msg + '\n' + block
print(msg)
