import requests
import time

users = [1, 2, 15889, 3, 1520373]

for i in range(len(users)):
    response = requests.post(f'http://localhost:4601/recommendations_offline?user_id={users[i]}&k=5')
    print("Status Code", response.status_code)
    if response.status_code != 200:
        break
    if i == 3:
        time.sleep(30)

    time.sleep(15)