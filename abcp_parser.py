
from selenium.webdriver.common.by import By

from .models import CatalogItem, save_catalog_data_to_db
from .uni_parser.universal_parser_firefox import WebsiteParser

# Ссылка на сайт
url_to_parse = "https://avtosnab161.ru/All_catalog"



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
        print(catalog_link)

    for i, link in enumerate(catalog_link):
        if i < 0:
            continue
        print(link)
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
                article_images = element2.find_elements(By.CLASS_NAME, 'article-image')
                image_link = ''
                if article_images:
                    image_links = article_images[0].find_elements(By.TAG_NAME, 'img')
                    if image_links:
                        image_link = image_links[0].get_attribute('src')
                articleDesc = element2.find_element(By.CLASS_NAME, 'articleDesc')
                articleDescATags = articleDesc.find_elements(By.TAG_NAME, 'a')
                brandName = articleDescATags[0].text
                brandLink = articleDescATags[0].get_attribute('data-href')
                index = articleDescATags[1].text
                indexSearch = articleDescATags[1].get_attribute('href')
                depiction = articleDescATags[2].text
                depictionLink = articleDescATags[2].get_attribute('href')
                catalog_data.append([image_link, brandName, index, indexSearch, depiction, depictionLink])
                print([image_link, brandName, index, indexSearch, depiction, depictionLink])
        for i in range(len(catalog_data)):
            depictionLink = catalog_data[i][5]
            with WebsiteParser(depictionLink) as parser3:
                print('Описание',depictionLink)

                image = ''
                images = parser3.find_elements([{'by': 'tag', 'value': 'img'}])
                if images:
                    image = images[0].get_attribute('src')
                InfoDescr = parser3.find_elements([{'by': 'class', 'value': 'goodsInfoDescr'}])[0].text
                characteristicsListRow = parser3.find_elements([{'by': 'class', 'value': 'characteristicsListRow'}])[0].text
                catalog_data[i].append(image)
                catalog_data[i].append(InfoDescr)
                catalog_data[i].append(characteristicsListRow)
                print([image, InfoDescr, characteristicsListRow])
        # Сохраняем данные в базу данных Django
        save_catalog_data_to_db(catalog_data)
        print(link, 'Сохранено')


if __name__ == '__main__':
    abcp_parser(url_to_parse)