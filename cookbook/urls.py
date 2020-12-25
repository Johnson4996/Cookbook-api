"""cookbook URL Configuration

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

from cookbookapi.views.cbuser import CbUsers
from cookbookapi.views.recipe import Recipes
from django.conf.urls import url
from django.conf.urls.static import static
from django.urls.conf import include
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token
from django.conf import settings
from cookbookapi.views import *


router = routers.DefaultRouter(trailing_slash=False)
router.register(r'recipes', Recipes, 'recipes')
router.register(r'userfavorites', UserFavorites, 'userfavorites')
router.register(r'categories', Categories, 'categories')
router.register(r'user', CbUsers, 'user')


urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^register$', register_user),
    url(r'^login$', login_user),
    url(r'^api-token-auth$', obtain_auth_token),
    url(r'^api-auth', include('rest_framework.urls', namespace='rest_framework')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)