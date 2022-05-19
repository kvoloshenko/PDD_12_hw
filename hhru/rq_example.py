import  requests
import pprint

DOMAIN = 'https://api.hh.ru/'

url_vacancies = f'{DOMAIN}vacancies'

# params = {'text': 'Python developer',
#           'page': 1}


# params = {'text': 'NAME:(Python OR AI) and (Django OR Keras)',
#           'page': 1}

params = {'text': 'NAME:(Python) and (AI OR ML OR Keras OR Numpy OR Pandas)',
          'page': 1}


result =  requests.get(url_vacancies, params = params).json()

# print(result.status_code)
# pprint.pprint(result)

items = result['items']
first = items[0]
# pprint.pprint(first)

print(first['alternate_url'])
print(first['url'])

one_vacancy_url = first['url']

result =  requests.get(one_vacancy_url, params = params).json()
pprint.pprint(result)