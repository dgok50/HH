import requests # для HTTP запросов
import matplotlib.pyplot as p
url = 'https://api.hh.ru/vacancies' # ссылка для работы с вакансиями (из API)
topic = ["machine learning", "data science", "big data", "data analytics"] # словарь для результата
topic_data = []
money = ["80к-", "80-120к", "120-150к", "150-200к", "200-300к", "300к+"]
money_data = [0, 0, 0, 0, 0, 0]
x = 0
pages = 10

for i in topic: # по темам словаря
    n = 0 # счетчик вакансий с указанной ЗП
    zp_all = 0
    for j in range(pages): # по страницам
        par = {'text': i,'per_page': '20', 'page': j} # параметры запроса
        x += 1
        print(int(x / (len(topic) * pages) * 100), "%")
        r = requests.get(url, par) # выполнение запроса
        e = r.json() # декодирование json
        y = e['items'] # информация о вакансиях с текущей страницы

        for k in y: # переберает вакансии текущей страницы
            if k['salary'] != None: #  есть ли общие данные по зарплате
                n += 1
                zp = 0
                s = k['salary'] # записываем общие данные по зарплате в переменную s
                if s['from'] != None and s['to'] != None: # есть ли данные по зп
                    zp = (s['from'] + s['to']) / 2
                elif s['from'] != None and s['to'] == None:
                    zp = s['from']
                elif s['from'] == None and s['to'] != None:
                    zp = s['to']
                zp_all += zp
                if zp < 80000:
                    money_data[0] += 1
                elif zp >= 80000 and zp < 120000:
                    money_data[1] += 1
                elif zp >= 120000 and zp < 150000:
                    money_data[2] += 1
                elif zp >= 150000 and zp < 200000:
                    money_data[3] += 1
                elif zp >= 200000 and zp < 300000:
                    money_data[4] += 1
                elif zp >= 300000:
                    money_data[5] += 1

    topic_data.append(int(zp_all / (n * 1000)))

p.bar(topic, topic_data)
p.show()
p.bar(money, money_data)
p.show()