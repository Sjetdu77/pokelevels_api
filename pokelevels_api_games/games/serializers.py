from rest_framework import serializers
from .models import *

class GameSerializer(serializers.ModelSerializer):
    associated_regions = serializers.StringRelatedField(many=True)
    accesses = serializers.PrimaryKeyRelatedField(many=True, queryset=Access.objects.all())

    class Meta:
        model = Game
        fields = ['id', 'name', 'generation', 'color', 'associated_regions', 'accesses']
        
class SpecieSerializer(serializers.ModelSerializer):
    wilds = serializers.StringRelatedField(many=True)

    class Meta:
        model = Specie
        fields = ['id', 'name', 'generation', 'sprite', 'xp', 'xp1_4', 'wilds']

class RegionSerializer(serializers.ModelSerializer):
    associated_games = serializers.StringRelatedField(many=True)

    class Meta:
        model = Region
        fields = ['id', 'name', 'associated_games']

class GameRegionSerializer(serializers.ModelSerializer):
    routes = serializers.StringRelatedField(many=True)
    game = serializers.SlugRelatedField(queryset=Game.objects.all(), slug_field='name')
    region = serializers.SlugRelatedField(queryset=Region.objects.all(), slug_field='name')

    class Meta:
        model = GameRegion
        fields = ['id', 'game', 'region', 'routes']

class RouteSerializer(serializers.ModelSerializer):
    wilds = serializers.StringRelatedField(many=True)
    game_region = serializers.PrimaryKeyRelatedField(queryset=GameRegion.objects.all())

    class Meta:
        model = Route
        fields = ['id', 'name', 'access', 'game_region', 'wilds']

class WildSerializer(serializers.ModelSerializer):
    route = serializers.PrimaryKeyRelatedField(queryset=Route.objects.all())
    specie = serializers.SlugRelatedField(slug_field='name', queryset=Specie.objects.all())

    class Meta:
        model = Wild
        fields = ['id', 'route', 'specie', 'probability', 'lvl', "mode", "time"]

class AccessSerializer(serializers.ModelSerializer):
    game = serializers.SlugRelatedField(queryset=Game.objects.all(), slug_field='name')

    class Meta:
        model = Access
        fields = ['id', 'game', 'number', 'name']