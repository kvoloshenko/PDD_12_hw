# Этот модуль предназначен для поиска вакансий на сайте HeadHunter с помощью API.
# Этот модуль позволяет быстро находить вакансии по заданным критериям и получать подробную информацию
# о конкретных вакансиях, используя API HeadHunter.

import  requests # Импортируем библиотеку для выполнения HTTP-запросов
import pprint    # Импортируем библиотеку для красивого вывода данных

DOMAIN = 'https://api.hh.ru/' # Доменный адрес API HeadHunter

url_vacancies = f'{DOMAIN}vacancies' # URL для получения списка вакансий

# params = {'text': 'Python developer',
#           'page': 1}


# params = {'text': 'NAME:(Python OR AI) and (Django OR Keras)',
#           'page': 1}

# Параметры запроса для поиска вакансий
params = {'text': 'NAME:(Python) and (AI OR ML OR Keras OR Numpy OR Pandas)',
          'page': 1}

# Выполняем GET-запрос к API для получения списка вакансий с указанными параметрами
result =  requests.get(url_vacancies, params = params).json()

# print(result.status_code)
# pprint.pprint(result)

# Извлекаем список вакансий из результата запроса
items = result['items']

# Извлекаем первую вакансию из списка
first = items[0]
# pprint.pprint(first)

# Печатаем URL страницы с подробной информацией о первой вакансии
print(first['alternate_url'])
print(first['url'])

# URL для получения полной информации о первой вакансии
one_vacancy_url = first['url']

# Выполняем GET-запрос к API для получения полной информации о первой вакансии
result =  requests.get(one_vacancy_url, params = params).json()
pprint.pprint(result)