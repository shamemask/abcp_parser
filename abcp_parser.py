from universal_parser_firefox import WebsiteParser
from selenium.webdriver.common.by import By

# Пример использования:
url_to_parse = "https://avtosnab161.ru/All_catalog"
geckodriver_path = 'C:\Windows\System32\geckodriver.exe'
with WebsiteParser(url_to_parse) as parser:

    # Укажите теги и атрибуты на каждом уровне вложенности для поиска
    tags_and_attributes = [
        {'by': 'class', 'value': 'fr-catalog-tile-inner'},
    ]

    result_elements = parser.find_elements(tags_and_attributes)

    catalog_link = []
    for element in result_elements:
        catalog_link.append(element.get_attribute('href'))

    print(catalog_link)

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

    print(catalog_data)

    depiction_data = []
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
    print(depiction_data)
