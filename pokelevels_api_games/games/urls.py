from django.urls import path
from games import views

urlpatterns = [
    path('games/', views.games, name='games'),
    path('games/<int:pk>/', views.game_detail, name='game-detail'),
    path('species/', views.species, name='species'),
    path('species/<str:pk>/', views.specie_detail, name='specie-detail'),
    path('routes/', views.routes, name='routes'),
    path('routes/<int:pk>/', views.route_detail, name='route-detail'),
    path('wilds/', views.wilds, name='wilds'),
    path('wilds/<int:pk>/', views.wild_detail, name='wild-detail'),
    path('regions/', views.regions, name='regions'),
    path('regions/<int:pk>/', views.region_detail, name='region-detail'),
    path('games_regions/', views.games_regions, name='games-regions'),
    path('games_regions/<int:pk>/', views.game_region_detail, name='game-region-detail'),
    path('fill_species/', views.fill_species, name='fill-species')
]