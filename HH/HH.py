import requests # для HTTP запросов
url = 'https://api.hh.ru/vacancies' # ссылка для работы с вакансиями (из API)
topic = {'machine learning': 0,"data science": 0,"big data": 0,"data analytics": 0} # словарь для результата
x = 0

for i in topic: # по темам словаря
    print(topic[i])
    zp = 0 # итоговая ЗП по конкретной теме
    n = 0 # счетчик вакансий с указанной ЗП
    for j in range(25): # по страницам
        x += 1
        print(x)
        par = {'text': i,'per_page': '10', 'page': j} # параметры запроса
        r = requests.get(url, par) # выполнение запроса
        e = r.json() # декодирование json
        try:
            y = e['items'] # информация о вакансиях с текущей страницы
        except:
            break

        for i in y: # переберает вакансии текущей страницы
            if i['salary'] != None: #  есть ли общие данные по зарплате
                n += 1
                s = i['salary'] # записываем общие данные по зарплате в переменную s
                if s['from'] != None and s['to'] != None: # есть ли данные по зп
                    zp += (s['from'] + s['to']) / 2
                elif s['from'] != None and s['to'] == None:
                    zp += s['from']
                elif s['from'] == None and s['to'] != None:
                    zp += s['to']

    # topic[i] = int(zp / n)

print(topic)