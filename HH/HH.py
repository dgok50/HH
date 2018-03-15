import requests # для HTTP запросов
url = 'https://api.hh.ru/vacancies' # ссылка для работы с вакансиями (из API)

for i in range(5): # по страницам сайта
    par = {'text': 'data analytics','per_page':'20', 'page':i} # параметры запроса
    r = requests.get(url, par) # выполнение запроса
    e = r.json() # декодирование json
    y = e['items'] # информация о вакансиях

    for i in y: # переберает вакансии
        print("job")
