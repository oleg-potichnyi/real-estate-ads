from django.db import models


class Scraper(models.Model):
    url = models.URLField(max_length=255)
    ad_title = models.CharField(max_length=255)
    region = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    description = models.TextField()
    image_urls = models.URLField(max_length=255, unique=True)
    publish_date = models.DateTimeField(auto_now_add=True)
    price = models.IntegerField()
    quantity_rooms = models.IntegerField()
    area = models.IntegerField()

    class Meta:
        ordering = ["ad_title"]

    def __str__(self) -> str:
        return self.ad_title
