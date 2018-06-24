from django.conf.urls import url, include
from django.urls import path
from rest_framework import routers
from .views import *
from rest_framework_swagger.views import get_swagger_view
schema_view = get_swagger_view(title='Pastebin API')
router = routers.DefaultRouter()
router.register(r'movies', MovieViewSet)
router.register(r'persons', PersonViewSet)
router.register(r'genre', GenreViewSet)
urlpatterns = [
url(r'^$', schema_view),
    url(r'^', include(router.urls)),
    path('search/',SearchView.as_view(),name='search'),
path('addmovie/',AddMovieView.as_view(),name='addmovie'),
path('editmovie/',EditMovieView.as_view(),name='editmovie'),
path('deletemovie/',DeleteMovieView.as_view(),name='deletemovie'),
path('login/',LoginView.as_view(),name='deletemovie'),



]