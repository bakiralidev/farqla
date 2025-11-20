# apps/bankapp/urls.py
from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views_clicks import go_redirect
from .views import CurrencyConvertAPIView


from .views import (
    BankViewSet, CardViewSet, CreditViewSet,
    DepositViewSet, CurrencyViewSet,
    AppViewSet, P2POfferViewSet
)

router = DefaultRouter()
router.register(r"banks", BankViewSet)
router.register(r"cards", CardViewSet)
router.register(r"credits", CreditViewSet)
router.register(r"deposits", DepositViewSet)
router.register(r"currencies", CurrencyViewSet)
router.register(r"apps", AppViewSet)
router.register(r"p2p-offers", P2POfferViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("go/<str:model_name>/<int:pk>/<str:field_name>/", go_redirect, name="go_redirect"),
    path("currency/convert/", CurrencyConvertAPIView.as_view(), name="currency-convert"),
]


