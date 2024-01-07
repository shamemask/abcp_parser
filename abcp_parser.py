
from selenium.webdriver.common.by import By

from models import CatalogItem, save_catalog_data_to_db
from uni_parser.universal_parser_firefox import WebsiteParser

# Ссылка на сайт
url_to_parse = "https://avtosnab161.ru/All_catalog"
# Путь к файлу geckodriver
geckodriver_path = 'C:\Windows\System32\geckodriver.exe'


def abcp_parser(avtosnab161_url):
    """
    Парсинг сайта avtosnab161.ru. Парсинг осуществляется с помощью библиотеки Selenium.
    Функция abcp_parser() принимает на вход URL-адрес сайта avtosnab161.ru.
    Запись данных в базу данных производится с помощью функции save_catalog_data_to_db().
    

    Args:
        avtosnab161_url (str): URL-адрес сайта avtosnab161.ru

    """
    # Очистка базы данных от объектов модели CatalogItem
    CatalogItem.objects.all().delete()
    with WebsiteParser(avtosnab161_url) as parser:
        # Укажите теги и атрибуты на каждом уровне вложенности для поиска
        tags_and_attributes = [
            {'by': 'class', 'value': 'fr-catalog-tile-inner'},
        ]

        result_elements = parser.find_elements(tags_and_attributes)

        catalog_link = []
        for element in result_elements:
            catalog_link.append(element.get_attribute('href'))


    for link in catalog_link:
        with WebsiteParser(link) as parser:
            tags_and_attributes2 = [
                {'by': 'class', 'value': 'item'},
            ]
            result_elements2 = parser.find_elements(tags_and_attributes2)
            catalog_data = []
            for element2 in result_elements2:
                tags_and_attributes3 = [
                    {'by': 'class', 'value': 'article-image'},
                    {'by': 'tag', 'value': 'img'},
                ]
                article_image = element2.find_element(By.CLASS_NAME, 'article-image')
                image_link = article_image.find_element(By.TAG_NAME, 'img').get_attribute('src')
                articleDesc = element2.find_element(By.CLASS_NAME, 'articleDesc')
                articleDescATags = articleDesc.find_elements(By.TAG_NAME, 'a')
                brandName = articleDescATags[0].text
                brandLink = articleDescATags[0].get_attribute('data-href')
                index = articleDescATags[1].text
                indexSearch = articleDescATags[1].get_attribute('href')
                depiction = articleDescATags[2].text
                depictionLink = articleDescATags[2].get_attribute('href')
                catalog_data.append([image_link, brandName, index, indexSearch, depiction, depictionLink])

        for i in range(len(catalog_data)):
            depictionLink = catalog_data[i][5]
            with WebsiteParser(depictionLink) as parser3:
                tags_and_attributes4 = [
                    {'by': 'class', 'value': 'article-image'},
                    {'by': 'class', 'value': 'goodsInfoDescr'},
                    {'by': 'class', 'value': 'characteristicsListRow'},
                ]
                result_elements3 = parser3.find_elements(tags_and_attributes4)
                catalog_data[i].append(result_elements3[0].find_element(By.TAG_NAME, 'img').get_attribute('src'))
                catalog_data[i].append(result_elements3[1].text)
                catalog_data[i].append(result_elements3[-1].text)

        # Сохраняем данные в базу данных Django
        save_catalog_data_to_db(catalog_data)


if __name__ == '__main__':
    abcp_parser(url_to_parse)