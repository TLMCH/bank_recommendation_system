import requests
import pandas as pd

# Скачивание файла
yandex_url = "https://disk.yandex.com/d/Io0siOESo2RAaA"
api_url = f"https://cloud-api.yandex.net/v1/disk/public/resources/download?public_key={yandex_url}"
response = requests.get(api_url)
download_url = response.json()['href']

# Сохранение на диск
r = requests.get(download_url)
with open('data/train_ver2.csv.zip', 'wb') as f:
    f.write(r.content)
print("Файл сохранён")

data = pd.read_csv('data/train_ver2.csv.zip', compression='zip', low_memory=False)
# запись данных в формате parquet для ускорения загрузки в дальнейшем
data.to_parquet("data/train_ver2.parquet")
print("Файл parquet сохранён")