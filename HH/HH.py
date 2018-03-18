import requests as r # HTTP запросы
import time
import progressbar
import matplotlib.pyplot as plt
import statistics
from collections import defaultdict

money = ["80к-", "80-120к", "120-150к", "150-200к", "200-300к", "300к+"]
topic = ["machine learning", "data science", "машинное обучение", "big data", "data analytics"] # словар запроса
val = {"KZT": 0.1788, "BYR": 29.3039, "EUR": 70.8099, "USD": 57.5043, "UAH": 2.196, "RUR": 1} # курс валют


base_url = 'https://api.hh.ru/' # ссылка для работы (из API)
vac_url = base_url + 'vacancies'
topic_data = []
regions_data = []
regions = []
mode = input("Select mode\n 1.Dev(4 pages, 20 vac per page)\n 2.1000vac\n 3.Custom\n")
if mode == '3':
	pages = int(input("Enter pages num:"))
	vac_perp = int(input("Enter vacancies per page num:"))
elif mode == '2':
	pages = 5
	vac_perp = 40
else:
	pages = 4
	vac_perp = 20
	
money_data = [0, 0, 0, 0, 0, 0]
max_progress = len(topic) * pages * vac_perp # рассчитываем максимальное значение прогресс бара

maxt = 0

for it in topic:
    par = {'text': it,'per_page': vac_perp, 'page': '0'} # параметры запроса
    maxt += int(r.get(vac_url, par).json()['found']) # выполнение запроса

if max_progress > maxt:
    max_progress = maxt

bprog = progressbar.ProgressBar(max_value=max_progress)
cprog = 0

zps = defaultdict(list)
zpe = defaultdict(list)
kids = 0
handicapped = 0

for i in topic: # по темам словаря
    n = 0 # счетчик вакансий с указанной ЗП
    all_zp = 0 # средняя ЗП по 1 теме
	
    par = {'text': i,'per_page': vac_perp, 'page': '0'} # параметры запроса
    mpages = int(r.get(vac_url, par).json()['pages']) # выполнение запроса
    if mpages < pages:
	    npages = mpages
    else:
        npages = pages
		
    for j in range(npages): # по страницам
        par = {'text': i, 'page': j, 'per_page': vac_perp} # параметры запроса
        m = r.get(vac_url, par).json()['items'] # выполнение запроса, декодирование json и переход к вакансиям
        for k in m: # переберает вакансии текущей страницы
            cprog += 1
            bprog.update(cprog)
            if k['salary'] == None: # есть ли общие данные по зарплате
                continue # прерывание
            s = k['salary'] # записываем общие данные по зарплате в переменную s
            if s["currency"] != "RUR" and s["currency"] != "KZT" and s["currency"] != "BYR" and s["currency"] != "EUR" and s["currency"] != "USD" and s["currency"] != "UAH": # проверяем валюту
                continue # прерывание

            if s["from"] != None and s["to"] != None: # если только конечная ЗП
                zp = (s['from'] + s['to']) / 2 * val[s["currency"]] # увеличение суммы ЗП по 1 теме
                n += 1 # вакансий с указанной ЗП
            elif s["from"] != None and s["to"] == None: # если только начальная ЗП
                if s["from"] * val[s["currency"]] >= 300000: # если ЗП более 300000
                    zp = s["from"] * val[s["currency"]] # ложная ЗП
                else: # иначе
                    continue # прерывание
            else: # иначе
                if s["to"] * val[s["currency"]] < 80000: # если ЗП до 80000
                    zp = s["to"] * val[s["currency"]]  # значение для 
                else: # иначе
                    continue # прерывание

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

            zps[k["name"]].append(zp)
			
            if 'accept_kids' in k:
                kids += int(k['accept_kids'])
				
            if 'accept_handicapped' in k:
                handicapped += int(k['accept_handicapped'])

            if 'area' in k:
              if isinstance(k['area'], dict):
                zpe[k["area"]["name"]].append(zp)
              elif isinstance(k['area'], list):
                    print(k['area'])
                    print()
                    for m in k['area']:
                        zpe[m["name"]].append(zp)

bprog.finish()

tzps = []
tzpe = []
print(cprog)

print(kids)
print(handicapped)
#print(zpe)
for i in zps:
    tzps.append(statistics.median(zps[i]))
	
for i in zpe:
    tzpe.append(statistics.median(zpe[i]))

gmode = 1
	
if gmode == 0:
 figure, bars = plt.subplots(2) # фигура с 2 элементами
 #plt.xticks(rotation = 90)
 bars[0].barh(money, money_data) # 2 гистограмма
 plt.gcf().subplots_adjust(left = 0.4)
 bars[1].barh(list(zps.keys()), tzps) # 1 гистограмма
 plt.show() # отображение гистограмм


if gmode == 1:
 plt.Figure()
 thismanager = plt.get_current_fig_manager()
 thismanager.window.wm_iconbitmap('hh.ico')

 plt.xlabel("Рубли")
 plt.ylabel("Количество вакансий") 
 plt.title("Зарплаты")
 plt.barh(money, money_data)
 plt.gcf().canvas.set_window_title('Зарплаты')
 plt.show()
#plt.xticks(rotation = 90)

 thismanager = plt.get_current_fig_manager()
 thismanager.window.wm_iconbitmap('hh.ico')
 plt.xlabel("Зарплата(Р)")
 plt.ylabel("Название вакансии") 
 plt.title("Распределение по вакансиям")
 plt.gcf().subplots_adjust(left = 0.4)
 plt.gcf().canvas.set_window_title('Распределение по вакансиям')
 plt.barh(list(zps.keys()), tzps)
 plt.show()
 
 thismanager = plt.get_current_fig_manager()
 thismanager.window.wm_iconbitmap('hh.ico')
 plt.xlabel("Зарплата(Р)")
 plt.ylabel("Регион") 
 plt.title("Распределение по регионам")
 plt.gcf().canvas.set_window_title('Распределение по регионам')
 plt.gcf().subplots_adjust(left = 0.4)
 plt.barh(list(zpe.keys()), tzpe)
 plt.show()
