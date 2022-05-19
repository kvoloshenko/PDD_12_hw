import  requests
import pprint

token = 'MY_TOKEN'

# Чтение файла
with open('token', 'r') as f:
    # 1. Прочитать сразу все данные
    token = f.read()
    print(token)

with open('login', 'r') as f:
    # 1. Прочитать сразу все данные
    login = f.read()
    print(login)

session = requests.Session()
session.auth = (login, token)

result = session.get('https://api.github.com/search/code?q=eval+in:file+language:python+user:DanteOnline')
print(result.status_code)

# Получение репозиториев

result = requests.get('https://api.github.com/search/repositories?q=swagger+language:python&sort=stars&order=desc')

pprint.pprint(result.json()['total_count'])
# pprint.pprint(result.json())

params = {
    'q': 'swagger+language:python',
    'sort': 'stars',
    'order': 'desc'
}
#
#
result = requests.get('https://api.github.com/search/repositories', params=params)
#
print(result.url)
#
pprint.pprint(result.json()['total_count'])
