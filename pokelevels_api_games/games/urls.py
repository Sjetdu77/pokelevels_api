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
    path('games_regions/<int:pk>/', views.game_region_detail, name='gameregion-detail'),
    path('accesses/', views.accesses, name='accesses'),
    path('accesses/<int:pk>/', views.accesses_detail, name='accesses-detail'),
    path('fill_species/', views.fill_species),
    path('fill_xp_species/', views.fill_xp_species),
    path('create_zones/', views.create_zones),
    path('routes_from_game/<int:game_id>', views.routes_from_game)
]