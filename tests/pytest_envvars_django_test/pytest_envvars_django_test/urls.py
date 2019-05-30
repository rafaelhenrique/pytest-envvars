from django.conf.urls import url
from core.views import ProductList

urlpatterns = [
    url(r'^$', ProductList.as_view(), name='product-list'),
]
