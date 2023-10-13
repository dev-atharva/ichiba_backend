from django.db import models

# Create your models here.


class ProductPackage(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    product_ids = models.CharField(max_length=255)


class Influencer(models.Model):
    name = models.CharField(max_length=255)
    product_recommendations = models.CharField(max_length=255)
    image_url = models.CharField(max_length=200)
    description = models.TextField()


class RecommendationList(models.Model):
    name = models.CharField(max_length=255)
    genre_ids = models.CharField(max_length=255)
    targeted_to = models.CharField(max_length=50)
