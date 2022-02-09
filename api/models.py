from django.db import models


class TOCHomepage(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    icon_url = models.URLField()
    category = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    data1_title = models.CharField(max_length=255)
    data1_url = models.URLField()
    data2_title = models.CharField(max_length=255)
    data2_url = models.URLField()
    data3_title = models.CharField(max_length=255)
    data3_url = models.URLField()
