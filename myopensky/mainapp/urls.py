from django.urls import path
from .views import show_fav, show_airplane, add_favorite, del_favorite

urlpatterns = [
    path('', show_fav),
    path('airplane/<str:icao24>/', show_airplane, name='airplane'),
    path('airplane/<str:icao24>/add', add_favorite),
    path('airplane/<str:icao24>/del', del_favorite)
]