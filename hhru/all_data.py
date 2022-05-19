import json
import pprint
import requests
import re


def data_save_json(data, file):
    with open(file, 'w', encoding='utf8') as f:
        json.dump(data, f)


def data_save_txt(data, file):
    with open(file, 'w', encoding='utf8') as f:
        f.write(data)


def get_params(keywords, page):
    params = {}
    params['text'] = keywords
    params['page'] = page
    # pprint.pprint(f'params={params}')
    return params


def request_get(url, params):
    result = requests.get(url, params=params)
    return result


def get_requirement_str(url_vacancies, params):
    result = request_get(url_vacancies, params)
    j_result = result.json()
    # data_save_json(j_result, 'rez_01.json')
    # print(result.status_code)
    # pprint.pprint(j_result)
    s_requirement = ''
    for item in j_result['items']:
        # pprint.pprint(f'item={item}')
        snippet = item['snippet']
        # pprint.pprint(f'snippet={snippet}')
        requirement = snippet['requirement']
        s_requirement += requirement + '\n'
        # pprint.pprint(f'requirement={requirement}')
    return s_requirement

def str_cliner(s_requirement):
    s_requirement = s_requirement.replace('<highlighttext>', '')
    s_requirement = s_requirement.replace('</highlighttext>', '')
    s_requirement = s_requirement.replace('-', '')
    s_requirement = s_requirement.replace('Apache Kafka', 'Apache_Kafka')
    s_requirement = s_requirement.replace('data leaks', 'data_leaks')
    s_requirement = s_requirement.replace('Spring Framework', 'Spring_Framework')
    s_requirement = s_requirement.replace('Spring Boot', 'Spring_Boot')
    s_requirement = s_requirement.replace('Netty framework', 'Netty_framework')
    s_requirement = s_requirement.replace('Java SE', 'Java_SE')
    s_requirement = s_requirement.replace('Spring MVC', 'Spring_MVC')
    s_requirement = s_requirement.replace('Spring Data JPA', 'Spring_Data_JPA')
    s_requirement = s_requirement.replace('Spring Security', 'Spring_Security')
    return s_requirement


def parser(keywords, s_requirement):
    all_data = {}
    all_data['keywords'] = keywords
    # выбираем слова через регулярные выражения
    p = re.compile("([a-zA-Z-_']+)")
    res = p.findall(s_requirement)
    # print(type(res), f'res={res}')
    # data_save_txt(res, 'res.txt')
    total_words = len(res)
    # print(f'total_words={total_words}')

    # создаем словарь. Ключ-слово, Значение-частота повторения
    lsWord = {}
    for key in res:
        key = key.lower()
        if key in lsWord:
            value = lsWord[key]
            lsWord[key] = value + 1
        else:
            lsWord[key] = 1

    # pprint.pprint(f'lsWord={lsWord}')

    # # создаем список ключей отсортированный по значению словаря lsWord
    # sorted_keys = sorted(lsWord, key=lambda x: int(lsWord[x]), reverse=True)
    sorted_l = sorted(lsWord.items(), key=lambda x: x[1], reverse=True)

    # pprint.pprint(f'sorted_l={sorted_l}')
    # all_data['count'] = len(sorted_l)

    requirements = []
    for item in sorted_l:
        i_dic = {}
        # print(f'item={item} item[0]={item[0]} item[1]={item[1]}')
        if int(item[1]) > 0:  # Не включаем низкочастотные слова
            i_dic['name'] = item[0]
            i_dic['count'] = item[1]
            i_dic['persent'] = int(item[1]) / total_words * 100
            requirements.append(i_dic)
            # print(i_dic)

    all_data['count'] = len(requirements)
    # print(f'requirements={requirements}')
    all_data['requirements'] = requirements
    return all_data

DOMAIN = 'https://api.hh.ru/'
url_vacancies = f'{DOMAIN}vacancies'
page = 1

# keywords = 'NAME:(Python) and (AI OR ML OR Keras OR Numpy OR Pandas)'
keywords_l = ['NAME:(Python) and (AI OR ML)',
              'NAME:(Python OR Java) AND COMPANY_NAME:(1 OR 2 OR YANDEX) AND (DJANGO OR SPRING)']
rez_data = []
i = 1
for keywords in keywords_l:
    params = get_params(keywords, page)
    s_requirement = get_requirement_str(url_vacancies, params)
    s_requirement = str_cliner(s_requirement)
    file_name=f'requirements_{i}.txt'
    data_save_txt(s_requirement, file_name)
    data = parser(keywords, s_requirement)
    rez_data.append(data)
    i+=1

data_save_json(rez_data, 'hhru_rezult.json')





