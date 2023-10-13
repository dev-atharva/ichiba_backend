from rest_framework import serializers
from .models import ProductPackage, RecommendationList, Influencer
import requests


class ItemSeralizer(serializers.Serializer):
    availability = serializers.IntegerField()
    genreId = serializers.CharField()
    itemCaption = serializers.CharField()
    itemName = serializers.CharField()
    itemPrice = serializers.CharField()
    itemUrl = serializers.URLField()
    rank = serializers.IntegerField()
    shopName = serializers.CharField()
    shopCode = serializers.CharField()
    imageUrl = serializers.URLField()


class ProductPackageSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    description = serializers.CharField()
    products = serializers.ListField(child=serializers.JSONField())

    def to_representation(self, instance):
        data = super().to_representation(instance)
        product_ids = instance.product_ids.split(",")

        product_details = []
        for product_id in product_ids:
            product_data = self.get_product_data_from_api(product_id)
            if product_data:
                product_details.append(product_data)

        data["products"] = product_details
        return data

    def get_product_data_from_api(self, product_id):
        api_url = f"https://app.rakuten.co.jp/services/api/IchibaItem/Search/20220601?format=json&itemCode={product_id}&applicationId=1018947431031079367"
        response = requests.get(api_url)
        if response.status_code == 200 and response.json()["hits"] >= 1:
            return response.json().get("Items", [])[0]["Item"]
        else:
            return "Not Found"


class RecommendationListSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecommendationList
        fields = "__all__"


class InfluencerSerialzer(serializers.ModelSerializer):
    class Meta:
        model = Influencer
        fields = ("name", "image_url", "id")
