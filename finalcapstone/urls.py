"""finalcapstoneapi URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""


from finalcapstoneapi.views.categories import Categories
from django.conf.urls import include
from django.urls import path
from django.conf import settings
from finalcapstoneapi.views import login_user, register_user
from finalcapstoneapi.views import ListedItems, Supply_Types, Listing_Types, Weight_Types, SoldItems, Expense
from rest_framework import routers

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'listeditems', ListedItems, 'listeditems')
router.register(r'solditems', SoldItems, 'solditems')
router.register(r'expenses', Expense, 'expenses')
router.register(r'categories', Categories, 'categories')
router.register(r'supply_types', Supply_Types, 'supply_types')
router.register(r'listing_types', Listing_Types, 'listing_types')
router.register(r'weight_types', Weight_Types, 'weight_types')

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth', include('rest_framework.urls', namespace='rest_framework')),
    path('login', login_user),
    path('register', register_user),
]
