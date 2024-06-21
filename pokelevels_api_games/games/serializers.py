from rest_framework import serializers
from .models import Game, Specie, Route, Wild, Region, GameRegion

class GameSerializer(serializers.HyperlinkedModelSerializer):
    associated_regions = serializers.HyperlinkedIdentityField(many=True, view_name='game-region-detail')

    class Meta:
        model = Game
        fields = ['id', 'name', 'generation', 'color', 'associated_regions']
        
class SpecieSerializer(serializers.HyperlinkedModelSerializer):
    wilds = serializers.HyperlinkedIdentityField(many=True, view_name='wild-detail')

    class Meta:
        model = Specie
        fields = ['id', 'name', 'generation', 'sprite', 'xp', 'xp1_4', 'wilds']

class RegionSerializer(serializers.HyperlinkedModelSerializer):
    associated_games = serializers.HyperlinkedIdentityField(many=True, view_name='game-region-detail')

    class Meta:
        model = Region
        fields = ['id', 'name', 'associated_games']

class GameRegionSerializer(serializers.HyperlinkedModelSerializer):
    routes = serializers.HyperlinkedIdentityField(many=True, view_name='route-detail')

    class Meta:
        model = GameRegion
        fields = ['id', 'game', 'region', 'routes']

class RouteSerializer(serializers.HyperlinkedModelSerializer):
    wilds = serializers.HyperlinkedIdentityField(many=True, view_name='wild-detail')

    class Meta:
        model = Route
        fields = ['id', 'name', 'access', 'game_region', 'wilds']

class WildSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Wild
        fields = ['id', 'route', 'specie', 'probability', 'lvlMin', 'lvlMax']