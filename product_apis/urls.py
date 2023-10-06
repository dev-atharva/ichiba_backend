from django.urls import path
from .views import (
    PopularItems,
    InfluencerProductRecommendations,
    ProductPackageDetailView,
    RecommendationListView,
    ProductListByGenre,
    InfluencerListApiView,
)

urlpatterns = [
    path("popular_items/", PopularItems.as_view(), name="Popular items"),
    path(
        "influencers/<int:influencer_id>/product-recommendations/",
        InfluencerProductRecommendations.as_view(),
        name="influencer-product-recommendations",
    ),
    path(
        "product-packages/<int:package_id>/",
        ProductPackageDetailView.as_view(),
        name="product-package-detail",
    ),
    path(
        "recommended-list/<int:list_id>/",
        RecommendationListView.as_view(),
        name="recommendation-lists",
    ),
    path(
        "product-genere-list/<int:genre_id>/",
        ProductListByGenre.as_view(),
        name="product-genere-list",
    ),
    path("influencers/", InfluencerListApiView.as_view(), name="influencer-list"),
]
