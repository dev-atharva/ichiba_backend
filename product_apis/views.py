from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Influencer, ProductPackage, RecommendationList
from rest_framework.generics import ListAPIView
from .serializers import (
    ProductPackageSerializer,
    RecommendationListSerializer,
    InfluencerSerialzer,
)
from .utils import get_genera_name
import requests


class PopularItems(APIView):
    def get(self, request):
        api_url = "https://app.rakuten.co.jp/services/api/IchibaItem/Ranking/20220601?format=json&applicationId=1018947431031079367"
        response = requests.get(api_url)
        if response.status_code == 200:
            data = response.json().get("Items", [])
            formatted_data = []
            for item in data:
                item_data = item.get("Item", {})
                if item_data.get("rank", None) >= 8 or None:
                    break
                if item_data.get("availability", None) == 0 or None:
                    continue
                formatted_item = {
                    # "availability": item_data.get("availability", None),
                    # "genreId": item_data.get("genreId", None),
                    # "itemCaption": item_data.get("itemCaption", None),
                    "itemName": item_data.get("itemName", None),
                    "itemPrice": item_data.get("itemPrice", None),
                    # "itemUrl": item_data.get("itemUrl", None),
                    "itemCode": item_data.get("itemCode", None),
                    "rank": item_data.get("rank", None),
                    # "shopName": item_data.get("shopName", None),
                    "shopCode": item_data.get("shopCode", None),
                    "imageUrl": item_data.get("mediumImageUrls", [{}])[0].get(
                        "imageUrl", None
                    ),
                }
                genra_parent = get_genera_name(int(item_data.get("genreId", None)))
                formatted_item["genreName"] = genra_parent
                formatted_data.append(formatted_item)
            return Response(formatted_data[:4])
        else:
            return Response(
                {"error": "Failed to fetch data from the third-party API"},
                status=response.status_code,
            )


class InfluencerProductRecommendations(APIView):
    def get(self, request, influencer_id):
        try:
            influencer = Influencer.objects.get(pk=influencer_id)
            product_ids = influencer.product_recommendations.split(",")
            products = []

            for product_id in product_ids:
                product_data = self.get_product_data_from_api(product_id)
                if product_data:
                    products.append(product_data)

            return Response(
                {
                    "products": products,
                    "name": influencer.name,
                    "image_url": influencer.image_url,
                }
            )
        except Influencer.DoesNotExist:
            return Response({"error": "Influencer does not exist."}, status=404)

    def get_product_data_from_api(self, product_id):
        api_url = f"https://app.rakuten.co.jp/services/api/IchibaItem/Search/20220601?format=json&itemCode={product_id}&applicationId=1018947431031079367"
        response = requests.get(api_url)

        if response.status_code == 200 and response.json()["hits"] >= 1:
            return response.json().get("Items", [])[0]["Item"]
        else:
            return "Not Found"


class ProductPackageDetailView(APIView):
    def get(self, request, package_id):
        try:
            package = ProductPackage.objects.get(pk=package_id)
            product_ids_str = package.product_ids
            product_ids_arr = product_ids_str.split(",")

            product_details = []
            for product_id in product_ids_arr:
                product_data = self.get_product_data_from_api(product_id)
                if product_data:
                    product_details.append(product_data)

            package_data = {
                "name": package.name,
                "description": package.description,
                "products": product_details,
            }

            return Response(package_data)
        except ProductPackage.DoesNotExist:
            return Response({"error": "Product package does not exist."}, status=404)

    def get_product_data_from_api(self, product_id):
        api_url = f"https://app.rakuten.co.jp/services/api/IchibaItem/Search/20220601?format=json&itemCode={product_id}&applicationId=1018947431031079367"
        response = requests.get(api_url)
        if response.status_code == 200 and response.json()["hits"] >= 1:
            return response.json().get("Items", [])[0]["Item"]
        else:
            return "Not Found"


class RecommendationListView(APIView):
    def get(self, request, list_id):
        lists = RecommendationList.objects.get(pk=list_id)
        genre_ids = [int(id) for id in lists.genre_ids.split(",")]
        products = self.get_products_for_genres(genre_ids)
        return Response(
            {
                "recommendation_list": lists.name,
                "products": products,
                "for_whom": lists.targeted_to,
            }
        )

    def get_products_for_genres(self, genre_ids):
        products = []
        genre_name_cache = {}  # Corrected variable name
        for genre_id in genre_ids:
            if genre_id in genre_name_cache:
                genre_name = genre_name_cache[genre_id]
            else:
                genre_name = self.get_genre_name(genre_id)
                genre_name_cache[genre_id] = genre_name
            products_for_genre = self.fetch_products_for_genre(genre_id)

            for product in products_for_genre:
                product["genreName"] = genre_name  # Corrected variable name
            products.extend(products_for_genre)
        return products

    def get_genre_name(self, genre_id):
        url = f"https://app.rakuten.co.jp/services/api/IchibaGenre/Search/20140222?format=json&genreId={int(genre_id)}&applicationId=1018947431031079367"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json().get("current", {})
            return data["genreName"]
        else:
            return ""

    def fetch_products_for_genre(self, genre_id):
        api_url = f"https://app.rakuten.co.jp/services/api/Product/Search/20170426?format=json&genreId={int(genre_id)}&applicationId=1018947431031079367"
        response = requests.get(api_url)

        if response.status_code == 200:
            data = response.json()
            products = data.get("Products", [])

            # Sort products by rank in descending order
            products.sort(key=lambda x: int(x["Product"]["rank"]), reverse=True)

            # Get the top 5 products
            top_5_products = products[:5]

            formatted_products = []
            for product in top_5_products:
                product_data = product["Product"]
                formatted_product = {
                    "productName": product_data["productName"],
                    "brandName": product_data["brandName"],
                    "genreName": product_data["genreName"],
                    "averagePrice": product_data["averagePrice"],
                    "maxPrice": product_data["maxPrice"],
                    "minPrice": product_data["minPrice"],
                    "productUrlPC": product_data["productUrlPC"],
                    "mediumImageUrl": product_data["mediumImageUrl"],
                    "productCaption": product_data["productCaption"],
                }
                formatted_products.append(formatted_product)

            return formatted_products
        else:
            return []


class ProductListByGenre(APIView):
    def get(self, request, genre_id):
        # Fetch products from the external API based on genre_id
        products = self.fetch_products_by_genre(genre_id)

        # Filter and sort products
        filtered_products = self.filter_and_sort_products(products)

        return Response(filtered_products)

    def fetch_products_by_genre(self, genre_id):
        # Make a request to your external API to fetch products based on genre_id
        api_url = f"https://app.rakuten.co.jp/services/api/IchibaItem/Search/20220601?format=json&genreId={genre_id}&applicationId=1018947431031079367"
        response = requests.get(api_url)

        if response.status_code == 200:
            data = response.json()
            items = data.get("Items", [])
            return items
        else:
            return []

    def filter_and_sort_products(self, products):
        # Filter and sort the products based on your criteria
        filtered_products = []

        for product in products:
            item = product.get("Item", {})
            item_data = {
                "itemName": item.get("itemName", ""),
                "itemPrice": item.get("itemPrice", 0),
                "reviewAverage": item.get("reviewAverage", 0),
                "itemUrl": item.get("itemUrl", ""),
            }
            filtered_products.append(item_data)

        sorted_products = sorted(
            filtered_products, key=lambda x: (x["itemPrice"], -x["reviewAverage"])
        )

        return sorted_products


class InfluencerListApiView(ListAPIView):
    queryset = Influencer.objects.all()
    serializer_class = InfluencerSerialzer
