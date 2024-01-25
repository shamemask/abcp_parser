
from selenium.webdriver.common.by import By

from .logging import logger
from .models import CatalogItem, save_item_to_db
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
    limit = 100
    logger.debug('abcp_parser is start')
    # Очистка базы данных от объектов модели CatalogItem
    # CatalogItem.objects.all().delete()

    # собрать все поля index из CatalogItem
    catalog_items = CatalogItem.objects.values_list('index', flat=True)

    with WebsiteParser(avtosnab161_url) as parser:
        # Укажите теги и атрибуты на каждом уровне вложенности для поиска
        tags_and_attributes = [
            {'by': 'class', 'value': 'fr-catalog-tile-inner'},
        ]

        result_elements = parser.find_elements(tags_and_attributes)

        catalog_link = []
        for element in result_elements:
            catalog_link.append(element.get_attribute('href'))
        logger.debug(catalog_link)

    for i, link in enumerate(reversed(catalog_link)):
        # if i < catalog_link.index('https://avtosnab161.ru/antiseptics_catalog'):
        #     continue
        logger.debug(link)
        for start in ['0',str(limit),str(2*limit),str(3*limit-1)]:
            with WebsiteParser(link+f'?limit={limit}&start={start}') as parser:
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
                    catalog = link.split('/')[-1]
                    articleDesc = element2.find_element(By.CLASS_NAME, 'articleDesc')
                    articleDescATags = articleDesc.find_elements(By.TAG_NAME, 'a')
                    brandName = articleDescATags[0].text
                    brandLink = articleDescATags[0].get_attribute('data-href')
                    index = articleDescATags[1].text
                    indexSearch = articleDescATags[1].get_attribute('href')
                    depiction = articleDescATags[2].text
                    depictionLink = articleDescATags[2].get_attribute('href')

                    # Проверка есть ли index в базе данных
                    if index in catalog_items:
                        continue

                    catalog_data.append([image_link, brandName, index, indexSearch, depiction, depictionLink])
                    logger.debug([catalog, image_link, brandName, index, indexSearch, depiction, depictionLink])
            for i in range(len(catalog_data)):
                depictionLink = catalog_data[i][-1]
                with WebsiteParser(depictionLink) as parser3:
                    logger.debug('Описание ' + depictionLink)

                    image = ''
                    article_images = parser3.find_elements([{'by': 'class', 'value': 'article-image'},])
                    if article_images:
                        images = article_images[0].find_elements(By.TAG_NAME, 'img')
                        image = images[0].get_attribute('src')

                    try:
                        goodsInfoDescr = parser3.find_elements([{'by': 'class', 'value': 'goodsInfoDescr'}])
                        InfoPrice = ''
                        if goodsInfoDescr:
                            InfoDescr = goodsInfoDescr[0].text
                        InfoPrice = parser3.find_elements([{'by': 'class', 'value': 'distrInfoPrice'}])
                        price = ''
                        if InfoPrice:
                            price = InfoPrice[0].text
                        characteristicsListRow = ''
                        characteristicsListRows = parser3.find_elements([{'by': 'class', 'value': 'characteristicsListRow'}])
                        characteristicsListRowsText = []
                        for row in characteristicsListRows:
                            characteristicsListRowsText.append(row.text)
                        characteristicsListRow = '\n'.join(characteristicsListRowsText) + '\n'
                        catalog_data[i].append(image)
                        catalog_data[i].append(InfoDescr)
                        catalog_data[i].append(characteristicsListRow)
                        catalog_data[i].append(catalog)
                        catalog_data[i].append(price)
                        logger.debug([image, InfoDescr, characteristicsListRow, price])
                        save_item_to_db(
                            image_link=catalog_data[i][0],
                            brand_name=catalog_data[i][1],
                            index=catalog_data[i][2],
                            index_search=catalog_data[i][3],
                            depiction=catalog_data[i][4],
                            depiction_link=catalog_data[i][5],
                            image_src=catalog_data[i][6],
                            characteristics=catalog_data[i][7],
                            other_info=catalog_data[i][8],
                            catalog=catalog_data[i][9],
                            price=catalog_data[i][10],
                        )
                        logger.debug('Сохранено ' + depictionLink)
                    except Exception as e:
                        logger.debug(f'Ошибка {depictionLink} - {e}')
            # Сохраняем данные в базу данных Django
            logger.debug(link + ' Сохранено')
    logger.debug('abcp_parser is end')

if __name__ == '__main__':
    abcp_parser(url_to_parse)