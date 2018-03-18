import requests as r # HTTP запросы
import matplotlib.pyplot as p # гистограммы
url = 'https://api.hh.ru/vacancies' # ссылка для работы с вакансиями (из API)
topic = ("machine learning", "data science", "big data", "data analytics") # список тем
topic_data = [] # средняя ЗП
money = ("80к-", "80-120к", "120-150к", "150-200к", "200-300к", "300к+") # список диапазонов ЗП
money_data = [0, 0, 0, 0, 0, 0] # количество вакансий

for i in topic: # по темам словаря
    n = 0 # счетчик вакансий с указанной ЗП
    zp_all = 0 # средняя ЗП по 1 теме
    for j in range(100): # по страницам
        par = {'text': i,'per_page': '20', 'page': j} # параметры запроса
        m = r.get(url, par).json()['items'] # выполнение запроса, декодирование json и переход к вакансиям

        for k in m: # переберает вакансии текущей страницы
            if k['salary'] != None: #  есть ли общие данные по зарплате
                n += 1 # вакансий с указанной ЗП
                zp = 0 # ЗП текущей вакансии
                s = k['salary'] # записываем общие данные по зарплате в переменную s
                if s['from'] != None and s['to'] != None: # есть полные данные
                    zp = (s['from'] + s['to']) / 2 # вычисление ЗП
                elif s['from'] != None and s['to'] == None: # 1 вид частичных данных
                    zp = s['from'] # вычисление ЗП
                elif s['from'] == None and s['to'] != None: # 2 вид частичных данных
                    zp = s['to'] # вычисление ЗП
                zp_all += zp # увеличение суммы ЗП по 1 теме

                if zp < 80000: # 1 диапазон
                    money_data[0] += 1 # + вакансия
                elif zp >= 80000 and zp < 120000: # 2 диапазон
                    money_data[1] += 1 # + вакансия
                elif zp >= 120000 and zp < 150000: # 3 диапазон
                    money_data[2] += 1 # + вакансия
                elif zp >= 150000 and zp < 200000: # 4 диапазон
                    money_data[3] += 1 # + вакансия
                elif zp >= 200000 and zp < 300000: # 5 диапазон
                    money_data[4] += 1 # + вакансия
                elif zp >= 300000: # 6 диапазон
                    money_data[5] += 1 # + вакансия

    topic_data.append(int(zp_all / (n * 1000))) # добавление средней ЗП по теме

figure, bars = p.subplots(2) # фигура с 2 элементами
bars[0].bar(topic, topic_data) # 1 гистограмма
bars[1].bar(money, money_data) # 2 гистограмма
p.show() # отображение гистограмм