import requests # для HTTP запросов
url = 'https://api.hh.ru/vacancies' # ссылка для работы с вакансиями (из API)
topic = ("machine learning", "data science", "big data", "data analytics") # словарь для результата
data = {"machine learning": 0, "data science": 0, "big data": 0, "data analytics": 0}
money = {"80к-": 0, "80-120к": 0, "120-150к": 0, "150-200к": 0, "200-300к": 0, "300к+": 0}
x = 0

for i in topic: # по темам словаря
    zp = 0 # итоговая ЗП по конкретной теме
    n = 0 # счетчик вакансий с указанной ЗП
    for j in range(20): # по страницам
        x += 1
        # print(x)
        par = {'text': i,'per_page': '20', 'page': j} # параметры запроса
        r = requests.get(url, par) # выполнение запроса
        e = r.json() # декодирование json
        try:
            y = e['items'] # информация о вакансиях с текущей страницы
        except:
            print("ВАКАНСИЙ НЕТ")
            break

        for k in y: # переберает вакансии текущей страницы
            if k['salary'] != None: #  есть ли общие данные по зарплате
                n += 1
                # print("ЗП не указана")
                s = k['salary'] # записываем общие данные по зарплате в переменную s
                if s['from'] != None and s['to'] != None: # есть ли данные по зп
                    zp += (s['from'] + s['to']) / 2
                elif s['from'] != None and s['to'] == None:
                    zp += s['from']
                elif s['from'] == None and s['to'] != None:
                    zp += s['to']
                print(zp)
                if zp < 80000:
                    money.update({"80к-": money["80к-"] + 1})
                elif zp >= 80000 and zp < 120000:
                    money.update({"80-120к": money["80-120к"] + 1})
                elif zp >= 120000 and zp < 150000:
                    money.update({"120-150к": money["120-150к"] + 1})
                elif zp >= 150000 and zp < 200000:
                    money.update({"150-200к": money["150-200к"] + 1})
                elif zp >= 200000 and zp < 300000:
                    money.update({"200-300к": money["200-300к"] + 1})
                elif zp >= 300000:
                    money.update({"300к+": money["300к+"] + 1})

    data.update({i: int(zp / (n * 1000))})

print(data)
print(money)