# Этот модуль предназначен для поиска вакансий на сайте HeadHunter с помощью API.
# Этот модуль позволяет быстро находить вакансии по заданным критериям и получать подробную информацию
# о конкретных вакансиях, используя API HeadHunter.

import  requests # Импортируем библиотеку для выполнения HTTP-запросов
import pprint    # Импортируем библиотеку для красивого вывода данных
from loguru import logger # Import logger
import time

DOMAIN = 'https://api.hh.ru/' # Доменный адрес API HeadHunter

url_vacancies = f'{DOMAIN}vacancies' # URL для получения списка вакансий


def get_vacancies(params):
    # Выполняем GET-запрос к API для получения списка вакансий с указанными параметрами
    result =  requests.get(url_vacancies, params = params).json()

    # print(result.status_code)
    # pprint.pprint(result)

    # Извлекаем список вакансий из результата запроса
    items = result['items']

    logger.debug(f'Найдено {len(items)} вакансий')
    i=1
    for item in items:
        department_name = 'Нет значения'
        if 'department' in item:
            department = item['department']
            # print(f'department_type={type(department)}')
            if department is not None and 'name' in department:
                department_name = department['name']

        print(f"{i}. {item['name']}-{department_name}--------------------")
        print(f"Ссылка: {item['alternate_url']}")
        logger.debug(f"{i}. {item['name']}-{department_name}--------------------")
        logger.debug(f"Ссылка: {item['alternate_url']}")

        pprint.pprint(item)
        i+=1

    # # Извлекаем первую вакансию из списка
    # first = items[0]
    # # pprint.pprint(first)
    #
    # # Печатаем URL страницы с подробной информацией о первой вакансии
    # print(first['alternate_url'])
    # print(first['url'])
    #
    # # URL для получения полной информации о первой вакансии
    # one_vacancy_url = first['url']
    #
    # # Выполняем GET-запрос к API для получения полной информации о первой вакансии
    # result =  requests.get(one_vacancy_url, params = params).json()
    # pprint.pprint(result)


if __name__ == "__main__":
    logger.add("Log/rq_example.log", format="{time} {level} {message}", level="DEBUG", rotation="100 KB",
               compression="zip")
    logger.debug('rq_example............')
    start_time = time.time()
    # Параметры запроса для поиска вакансий
    # params = {'text': 'Python developer', 'page': 1}
    # params = {'text': 'NAME:(Python OR AI) and (Django OR Keras)',  'page': 1}
    # params = {'text': 'NAME:(Python) and (AI OR ML OR Keras OR Numpy OR Pandas)', 'page': 1}
    params = {'text': 'NAME:(Аналитик OR Бизнес аналитик OR Системный аналитик OR Analyst OR Business Analyst OR System Analyst) '
                      'and (AI OR ChatGPT OR LLM OR prompt OR  openai OR  langchain)'}
    logger.debug(f'params = {params}')
    get_vacancies(params)

    end_time = time.time()
    elapsed_time = end_time - start_time
    logger.debug(f'rq_example elapsed_time = {elapsed_time} sec')
