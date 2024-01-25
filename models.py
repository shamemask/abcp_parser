from django.db import models

class CatalogItem(models.Model):
    image_link = models.CharField(max_length=200)
    brand_name = models.CharField(max_length=100)
    index = models.CharField(max_length=50)
    index_search = models.CharField(max_length=200)
    depiction = models.CharField(max_length=200)
    depiction_link = models.CharField(max_length=200)
    image_src = models.CharField(max_length=200)
    characteristics = models.TextField()
    other_info = models.TextField()
    catalog = models.CharField(max_length=200)
    price = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.brand_name} - {self.index}"

def save_item_to_db(
        image_link,
        brand_name,
        index,
        index_search,
        depiction,
        depiction_link,
        image_src,
        characteristics,
        other_info,
        catalog,
        price
):
    catalog_item = CatalogItem(
        image_link=image_link,
        brand_name=brand_name,
        index=index,
        index_search=index_search,
        depiction=depiction,
        depiction_link=depiction_link,
        image_src=image_src,
        characteristics=characteristics,
        other_info=other_info,
        catalog=catalog,
        price=price
    )
    catalog_item.save()

# Сохранение данных в базу
def save_list_to_db(data):
    for entry in data:
        catalog_item = CatalogItem(
            image_link=entry[0],
            brand_name=entry[1],
            index=entry[2],
            index_search=entry[3],
            depiction=entry[4],
            depiction_link=entry[5],
            image_src=entry[6],
            characteristics=entry[7],
            other_info=entry[8],
            catalog=entry[9],
            price=entry[10]
        )
        catalog_item.save()
