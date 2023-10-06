from django.contrib import admin
from .models import ProductPackage, Influencer, RecommendationList

# Register your models here.

admin.site.register(ProductPackage)
admin.site.register(Influencer)
admin.site.register(RecommendationList)
