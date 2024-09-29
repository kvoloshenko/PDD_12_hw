# Этот модуль предназначен для извлечения, обработки и анализа данных о вакансиях с сайта HH.ru.
# Основная цель заключается в сборе требований к вакансиям с использованием заданных ключевых слов,
# очистке этих данных, а затем анализе частоты встречаемости ключевых слов в требованиях.
# Результаты сохраняются в JSON файл для дальнейшего анализа.
# Этот модуль полезен для подготовки данных и анализа требований к вакансиям в автоматическом режиме,
# что может быть полезно для рекрутеров или аналитиков рынка труда.

# Импортируемые библиотеки
import json       # Для работы с JSON файлом
import pprint     # Для форматированного вывода на консоль
import requests   # Для выполнения HTTP-запросов
import re         # Для работы с регулярными выражениями
from loguru import logger # Import logger
import time


def data_save_json(data, file):
    '''
    Сохраняет данные в JSON файл.
    :param data: данные для сохранения.
    :param file: имя файла.
    '''
    with open(file, 'w', encoding='utf8') as f:
        json.dump(data, f)


def data_save_txt(data, file):
    '''
    Сохраняет данные в текстовый файл.
    :param data: данные для сохранения.
    :param file: имя файла.
    '''
    with open(file, 'w', encoding='utf8') as f:
        f.write(data)


def get_params(keywords, page):
    '''
    Формирует словарь параметров для запроса, содержащий ключевые слова и номер страницы.
    :param keywords: строка ключевых слов для поиска.
    :param page:  номер страницы для получения результатов.
    :return: словарь параметров для запроса
    '''
    params = {}
    params['text'] = keywords
    params['page'] = page
    # pprint.pprint(f'params={params}')
    return params


def request_get(url, params):
    '''
    Выполняет GET-запрос на заданный URL с указанными параметрами
    :param url: адрес для запроса.
    :param params: словарь параметров для запроса.
    :return: результат запроса
    '''
    result = requests.get(url, params=params)
    return result


def get_requirement_str(url_vacancies, params):
    '''
    Получает данные о вакансиях и извлекает требования к ним
    :param url_vacancies: URL для получения данных о вакансиях
    :param params: параметры запроса.
    :return: Возвращает строку с требованиями всех полученных вакансий.
    '''
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
    '''
    Очищает строку требований, заменяя определенные подстроки.
    :param s_requirement: строка требований.
    :return: Возвращает очищенную строку.
    '''
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
    '''
    Анализирует строку требований, выделяет ключевые слова и считает их частоту.
    :param keywords: ключевые слова для поиска.
    :param s_requirement: строка требований.
    :return: Возвращает словарь с результатами анализа.
    '''
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

DOMAIN = 'https://api.hh.ru/'        # базовый URL для API HH.ru
url_vacancies = f'{DOMAIN}vacancies' # полный URL для получения данных о вакансиях.
page = 1                             # номер страницы для получения данных

def run (keywords_l):
    '''
    Основной цикл обработки данных
        - Итерируется по списку `keywords_l`.
        - Параметры запроса формируются функцией `get_params`.
        - Данные о требованиях к вакансиям извлекаются с помощью `get_requirement_str`.
        - Строка требований очищается с помощью `str_cliner`.
        - Очищенные данные сохраняются в текстовый файл.
        - Результаты анализа сохраняются в JSON файл `hhru_rezult.json`.
    '''
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


if __name__ == "__main__":
    logger.add("Log/all_data.log", format="{time} {level} {message}", level="DEBUG", rotation="100 KB",
               compression="zip")
    logger.debug('all_data............')
    start_time = time.time()
    # Список ключевых слов для поиска
    keywords_l = ['NAME:(Аналитик OR Бизнес аналитик OR Системный аналитик OR Analyst OR Business Analyst OR System Analyst) '
                      'and (AI OR ChatGPT OR LLM OR prompt OR  openai OR  langchain)',
                'NAME:(Аналитик) and (ChatGPT)',
                'NAME:(Python) and (ChatGPT)',
                'NAME:(Python) and (AI OR ML)',
                'NAME:(Python OR Java) AND COMPANY_NAME:(1 OR 2 OR YANDEX) AND (DJANGO OR SPRING)']

    run(keywords_l)
    end_time = time.time()
    elapsed_time = end_time - start_time
    logger.debug(f'all_data elapsed_time = {elapsed_time} sec')





