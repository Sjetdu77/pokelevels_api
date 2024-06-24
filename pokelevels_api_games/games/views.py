from urllib import request as R
# parsing data from the client
from rest_framework.parsers import JSONParser
from rest_framework.request import Request
# To bypass having a CSRF token
from django.views.decorators.csrf import csrf_exempt
# for sending response to the client
from django.http import HttpResponse, JsonResponse
from bs4 import BeautifulSoup
from .models import Game, Specie, Route, Wild, Region, GameRegion
from .serializers import GameSerializer, SpecieSerializer, RouteSerializer, WildSerializer, RegionSerializer, GameRegionSerializer

import requests

# Create your views here.
@csrf_exempt
def games(request):
    if (request.method == 'GET'):
        games = Game.objects.all()
        serializer = GameSerializer(games, many=True, context={ 'request': Request(request) })
        return JsonResponse(serializer.data, safe=False)
    
    elif (request.method == 'POST'):
        data = JSONParser().parse(request)
        serializer = GameSerializer(data=data, context={ 'request': Request(request) })
        if (serializer.is_valid()):
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        
    return JsonResponse(serializer.errors, status=400)

@csrf_exempt
def game_detail(request, pk):
    try:
        game = Game.objects.get(pk=pk)
    except:
        return HttpResponse(status=404)
    
    if (request.method == "GET"):
        serializer = GameSerializer(game, context={ 'request': Request(request) })
        print(game)
        return JsonResponse(serializer.data, status=201)
    
    elif (request.method == 'PUT'):
        data = JSONParser().parse(request)
        serializer = GameSerializer(game, data=data, context={ 'request': Request(request) })

        if (serializer.is_valid()):
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        
        return JsonResponse(serializer.errors, status=404)
    
    elif(request.method == 'DELETE'):
        game.delete()
        return HttpResponse(status=204)

@csrf_exempt
def species(request):
    if (request.method == 'GET'):
        species = Specie.objects.all()
        serializer = SpecieSerializer(species, many=True, context={ 'request': Request(request) })
        return JsonResponse(serializer.data, safe=False)
    
    elif (request.method == 'POST'):
        data = JSONParser().parse(request)
        serializer = SpecieSerializer(data=data, context={ 'request': Request(request) })
        if (serializer.is_valid()):
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        
    return JsonResponse(serializer.errors, status=400)

@csrf_exempt
def specie_detail(request, pk):
    try:
        specie = Specie.objects.get(pk=pk)
    except:
        return HttpResponse(status=404)
    
    if (request.method == 'GET'):
        serializer = SpecieSerializer(specie, context={ 'request': Request(request) })
        return JsonResponse(serializer.data, status=201)
    
    elif (request.method == 'PUT'):
        data = JSONParser().parse(request)

        try: data['id']
        except: data['id'] = specie.id

        try: data['name']
        except: data['name'] = specie.name

        try: data['generation']
        except: data['generation'] = specie.generation

        try: data['sprite']
        except: data['sprite'] = specie.sprite

        try: data['wilds']
        except: data['wilds'] = []

        serializer = SpecieSerializer(specie, data=data, context={ 'request': Request(request) })

        if (serializer.is_valid()):
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        
        return JsonResponse(serializer.errors, status=404)
    
    elif(request.method == 'DELETE'):
        specie.delete()
        return HttpResponse(status=204)
    
@csrf_exempt
def routes(request):
    if (request.method == 'GET'):
        games = Route.objects.all()
        serializer = RouteSerializer(games, many=True, context={ 'request': Request(request) })
        return JsonResponse(serializer.data, safe=False)
    
    elif (request.method == 'POST'):
        data = JSONParser().parse(request)
        serializer = RouteSerializer(data=data, context={ 'request': Request(request) })
        if (serializer.is_valid()):
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        
    return JsonResponse(serializer.errors, status=400)

@csrf_exempt
def route_detail(request, pk):
    try:
        route = Route.objects.get(pk=pk)
    except:
        return HttpResponse(status=404)
    
    if (request.method == 'GET'):
        serializer = RouteSerializer(route, context={ 'request': Request(request) })
        JsonResponse(serializer.data, status=201)
    
    elif (request.method == 'PUT'):
        data = JSONParser().parse(request)
        serializer = RouteSerializer(route, data=data, context={ 'request': Request(request) })

        if (serializer.is_valid()):
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        
        return JsonResponse(serializer.errors, status=404)
    
    elif(request.method == 'DELETE'):
        route.delete()
        return HttpResponse(status=204)

@csrf_exempt
def wilds(request):
    if (request.method == 'GET'):
        wilds = Wild.objects.all()
        serializer = WildSerializer(wilds, many=True, context={ 'request': Request(request) })
        return JsonResponse(serializer.data, safe=False)
    
    elif (request.method == 'POST'):
        data = JSONParser().parse(request)
        serializer = WildSerializer(data=data, context={ 'request': Request(request) })
        if (serializer.is_valid()):
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        
    return JsonResponse(serializer.errors, status=400)

@csrf_exempt
def wild_detail(request, pk):
    try:
        wild = Wild.objects.get(pk=pk)
    except:
        return HttpResponse(status=404)
    
    if (request.method == 'GET'):
        serializer = WildSerializer(wild, context={ 'request': Request(request) })
        return JsonResponse(serializer.data, status=201)
    
    if (request.method == 'PUT'):
        data = JSONParser().parse(request)
        serializer = WildSerializer(wild, data=data, context={ 'request': Request(request) })

        if (serializer.is_valid()):
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        
        return JsonResponse(serializer.errors, status=404)
    
    elif(request.method == 'DELETE'):
        wild.delete()
        return HttpResponse(status=204)
    
@csrf_exempt
def regions(request):
    if (request.method == 'GET'):
        regions = Region.objects.all()
        serializer = RegionSerializer(regions, many=True, context={ 'request': Request(request) })
        return JsonResponse(serializer.data, safe=False)
    
    elif (request.method == 'POST'):
        data = JSONParser().parse(request)
        serializer = RegionSerializer(data=data, context={ 'request': Request(request) })
        if (serializer.is_valid()):
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        
    return JsonResponse(serializer.errors, status=400)

@csrf_exempt
def region_detail(request, pk):
    try:
        region = Region.objects.get(pk=pk)
    except:
        return HttpResponse(status=404)
    
    if (request.method == 'GET'):
        serializer = RegionSerializer(region, context={ 'request': Request(request) })
        return JsonResponse(serializer.data, status=201)
    
    elif (request.method == 'PUT'):
        data = JSONParser().parse(request)
        serializer = RegionSerializer(region, data=data, context={ 'request': Request(request) })

        if (serializer.is_valid()):
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        
        return JsonResponse(serializer.errors, status=404)
    
    elif(request.method == 'DELETE'):
        region.delete()
        return HttpResponse(status=204)
    
@csrf_exempt
def games_regions(request):
    if (request.method == 'GET'):
        games_regions = GameRegion.objects.all()
        serializer = GameRegionSerializer(games_regions, many=True, context={ 'request': Request(request) })
        return JsonResponse(serializer.data, safe=False)

    elif (request.method == 'POST'):
        data = JSONParser().parse(request)
        serializer = GameRegionSerializer(data=data, context={ 'request': Request(request) })
        if (serializer.is_valid()):
            serializer.save()
            return JsonResponse(serializer.data, status=201)

    return JsonResponse(serializer.errors, status=400)

@csrf_exempt
def game_region_detail(request, pk):
    try:
        game_region = GameRegion.objects.get(pk=pk)
    except:
        return HttpResponse(status=404)
    
    if (request.method == 'GET'):
        serializer = GameRegionSerializer(game_region, context={ 'request': Request(request) })
        JsonResponse(serializer.data, status=201)

    elif (request.method == 'PUT'):
        data = JSONParser().parse(request)
        serializer = GameRegionSerializer(game_region, data=data, context={ 'request': Request(request) })

        if (serializer.is_valid()):
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        
        return JsonResponse(serializer.errors, status=404)
    
    elif(request.method == 'DELETE'):
        game_region.delete()
        return HttpResponse(status=204)

@csrf_exempt
def fill_species(request):
    if (request.method == 'POST'):
        f = requests.get("https://tyradex.vercel.app/api/v1/pokemon")
        objects = {
            'datas': []
        }
        for data in f.json():
            if data['pokedex_id'] > 0:
                try:
                    specie = Specie.objects.get(id=data['pokedex_id'])
                    objects['datas'].append(specie)
                    print(specie)
                except:
                    sprite = requests.get(data['sprites']['regular']).content
                    with open(f'C:/Users/destr/Documents/pokelevels_api/pokelevels_client/src/assets/sprites/{data['pokedex_id']}.png', 'wb+') as handler:
                        handler.write(sprite)

                    neededData = {
                        'id': "{:04d}".format(data['pokedex_id']),
                        'name': data['name']['fr'],
                        'generation': data['generation'],
                        'sprite': f'./assets/sprites/{data['pokedex_id']}.png',
                        'wilds': []
                    }

                    serializer = SpecieSerializer(data=neededData)
                    if (serializer.is_valid()):
                        serializer.save()
                        objects['datas'].append(serializer.data)
                        print(serializer.data)
                    else: return JsonResponse(serializer.errors, status=404)

        return JsonResponse(objects, status=201)
    
    elif (request.method == 'DELETE'):
        Specie.objects.all().delete()
        return JsonResponse({}, status=201)
    
    return JsonResponse({ 'error': 'No corresponding method' }, status=404)

@csrf_exempt
def fill_xp_species(request):
    if request.method == 'GET':
        objects = {}
        headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36"}

        request_ix = R.Request('https://bulbapedia.bulbagarden.net/wiki/List_of_Pok%C3%A9mon_by_effort_value_yield_(Generation_IX)', headers=headers)
        site_ix = R.urlopen(request_ix).read()
        soup_site_ix = BeautifulSoup(str(site_ix), features="html.parser")
        pokelist_ix = soup_site_ix.find_all('table')[1]

        for mon in pokelist_ix.find_all('tr'):
            tds = mon.find_all('td')
            if len(tds) > 0:
                specie_id = tds[0].text.replace('\\n', '')
                specie_xp = int(tds[3].text.replace('\\n', ''))

                specie = Specie.objects.get(id=specie_id)
                neededData = {
                    'id': specie.id,
                    'name': specie.name,
                    'generation': specie.generation,
                    'sprite': specie.sprite,
                    'xp': specie_xp,
                    'wilds': []
                }

                serializer = SpecieSerializer(specie, data=neededData)

                if serializer.is_valid():
                    serializer.save()
                else: return JsonResponse(serializer.errors, status=402)

        request_iv = R.Request('https://bulbapedia.bulbagarden.net/wiki/List_of_Pok%C3%A9mon_by_effort_value_yield_(Generation_IV)', headers=headers)
        site_iv = R.urlopen(request_iv).read()
        soup_site_iv = BeautifulSoup(str(site_iv), features="html.parser")
        pokelist_iv = soup_site_iv.find_all('table')[1]

        for mon in pokelist_iv.find_all('tr'):
            tds = mon.find_all('td')
            if len(tds) > 0:
                specie_id = tds[0].text.replace('\\n', '')
                specie_xp = int(tds[3].text.replace('\\n', ''))

                specie = Specie.objects.get(id=specie_id)
                neededData = {
                    'id': specie.id,
                    'name': specie.name,
                    'generation': specie.generation,
                    'sprite': specie.sprite,
                    'xp1_4': specie_xp,
                    'wilds': []
                }

                serializer = SpecieSerializer(specie, data=neededData)
                if serializer.is_valid():
                    serializer.save()
                    objects[specie_id] = serializer.data
                else: return JsonResponse(serializer.errors, status=402)

        return JsonResponse(objects, status=201)
    
    return JsonResponse({ 'error': 'No corresponding method' }, status=404)

@csrf_exempt
def create_zones(request):
    if request.method == 'GET':
        objects = {}

        allGamesRegions = {
            "Kanto": {
                "Routes": {
                    "1": range(1, 26),
                    "2": range(1, 29),
                    "3": range(1, 26),
                    "4": range(1, 29),
                    "7": range(1, 26),
                },
                "Games": [
                    "Rouge",
                    "Bleu",
                    "Jaune",
                    "Or",
                    "Argent",
                    "RougeFeu",
                    "VertFeuille",
                    "HeartGold",
                    "SoulSilver",
                    "Let's Go Pikachu",
                    "Let's Go Evoli"
                ]
            },
            "Johto": {
                "Routes": {
                    "2": range(29, 47),
                    "4": range(29, 47)
                },
                "Games": [
                    "Or",
                    "Argent",
                    "HeartGold",
                    "SoulSilver"
                ]
            },
            "Hoenn": {
                "Routes": {
                    "3": range(101, 135),
                    "6": range(101, 135)
                },
                "Games": [
                    "Rubis",
                    "Saphir",
                    "Emeraude",
                    "Rubis Oméga",
                    "Saphir Alpha",
                ]
            },
            "Sinnoh": {
                "Routes": {
                    "4": range(201, 231),
                    "8": range(201, 231)
                },
                "Games": [
                    "Diamant",
                    "Perle",
                    "Diamant Etincelant",
                    "Perle Scintillante",
                    "Légendes : Arceus"
                ]
            },
            "Unys": {
                "Routes": {
                    "5": range(1, 18)
                },
                "Games": [
                    "Noir",
                    "Blanc",
                    "Noir 2",
                    "Blanc 2"
                ]
            },
            "Kalos": {
                "Routes": {
                    "6": range(1, 22)
                },
                "Games": [
                    "X",
                    "Y"
                ]
            },
            "Alola": {
                "Routes": {
                    "7": range(1, 17)
                },
                "Games": [
                    "Soleil",
                    "Lune",
                    "Ultra-Soleil",
                    "Ultra-Lune"
                ]
            },
            "Galar": {
                "Routes": {
                    "8": range(1, 11)
                },
                "Games": [
                    "Epée",
                    "Bouclier"
                ]
            }
        }

        for region in allGamesRegions:
            here = allGamesRegions[region]
            here["Region"] = Region.objects.get(name=region)
            here["Games Datas"] = {}

            for game in here["Games"]:
                this_game = Game.objects.get(name=game)
                here["Games Datas"][game] = {
                    "Game": this_game,
                    "Game Region": GameRegion.objects.get(game=this_game.id, region=here["Region"].id)
                }

        for region in allGamesRegions:
            here = allGamesRegions[region]

            for game in here["Games"]:
                data_game = here["Games Datas"][game]

                try:
                    for i in here["Routes"][str(data_game["Game"].generation)]:
                        data = {
                            "name": f"Route {i}",
                            "game_region": f"http://127.0.0.1:8000/api/games_regions/{data_game["Game Region"].id}/",
                            "wilds": []
                        }
                        
                        serializer = RouteSerializer(data=data, context={ 'request': Request(request) })
                        if (serializer.is_valid()):
                            serializer.save()
                            objects[serializer.data['id']] = serializer.data
                        else: return JsonResponse(serializer.errors, status=500)
                except: print("No gen")

        return JsonResponse(objects, status=201)
    
    elif request.method == 'DELETE':
        Route.objects.all().delete()
        return JsonResponse({}, status=201)
    
    return JsonResponse({ 'error': 'No corresponding method' }, status=404)