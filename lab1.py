import subprocess
import re
import csv


def ping(address):
    reply = subprocess.run(['ping', '-n', '1', address],
                           stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE,
                           encoding='cp866') #Запускаем команду 'ping -n 1 <address>
    if reply.returncode == 0: # если есть ответ -> возвращаем его
        return reply.stdout
    else:
        return reply.stderr

def parse_rtt(reply):
    match = re.search(r'время=(\d+)', reply) #парсим всё что после "время="
    if match:
        return int(match.group(1)) # Нашли -> сохранили и вернули
    return None


def save_to_csv(data, filename="ping_results.csv"):
    with open(filename, mode='w', newline='', encoding='utf-8') as file: #Открыли для записи(w)
        writer = csv.writer(file) # Создали "писателя"
        writer.writerow(["Сайт", "Время (мс)"]) # записываем строки
        writer.writerows(data)
        
websites = ['yandex.ru',
            'mail.ru',
            'vk.com',
            'twitch.tv',
            'ozon.ru',
            'rambler.ru',
            'dns-shop.ru',
            'banki.ru',
            'wildberries.ru',
            'ok.ru']

results = []

for website in websites:
        output = ping(website) # Пингуем
        rtt = parse_rtt(output) # Парсим
        if rtt is not None:
            print(f"Сайт: {website}, Время: {rtt} мс")
            results.append([website, rtt]) 
        else:
            print(f"Не удалось получить время для сайта: {website}")

save_to_csv(results)
