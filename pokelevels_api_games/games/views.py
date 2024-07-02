from urllib import request as R
# parsing data from the client
from rest_framework.parsers import JSONParser
from rest_framework.request import Request
# To bypass having a CSRF token
from django.views.decorators.csrf import csrf_exempt
# for sending response to the client
from django.http import HttpResponse, JsonResponse
from bs4 import BeautifulSoup
from .models import *
from .serializers import *

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
        data['associated_regions'] = []
        data['accesses'] = []
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
        data['wilds'] = []
        serializer = SpecieSerializer(data=data, context={ 'request': Request(request) })
        if (serializer.is_valid()):
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        
    return JsonResponse(serializer.errors, status=400)

@csrf_exempt
def specie_detail(request, pk):
    try:
        int(pk)
        specie = Specie.objects.get(pk="{:04d}".format(int(pk)))
    except:
        try:
            specie = Specie.objects.get(name=pk)
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
        data['wilds'] = []
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
        return JsonResponse(serializer.data, status=201)
    
    elif (request.method == 'PUT'):
        data = JSONParser().parse(request)

        try: data['name']
        except: data['name'] = route.name

        try: data['game_region']
        except: data['game_region'] = route.game_region.id

        try: data['wilds']
        except:
            wilds = []
            for w in route.wilds.all():
                wilds.append(f"http://127.0.0.1:8000/api/wilds/{w.id}/")

            data['wilds'] = wilds

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
        allWilds = {}
        for aWild in serializer.data:
            allWilds[aWild['id']] = aWild
        return JsonResponse(allWilds)
    
    elif (request.method == 'POST'):
        data = JSONParser().parse(request)
        if (type(data) == dict):
            try:
                all_objects = []
                for aWild in data['wilds']:
                    aWild['route'] = data['route']
                    serializer = WildSerializer(data=aWild, context={ 'request': Request(request) })
                    if (serializer.is_valid()):
                        serializer.save()
                        all_objects.append(serializer.data)
                    else:
                        return JsonResponse(serializer.errors, status=402)
                return JsonResponse({
                    "route": data['route'],
                    "objects": all_objects
                }, status=201)
            
            except:
                serializer = WildSerializer(data=data, context={ 'request': Request(request) })
                if (serializer.is_valid()):
                    serializer.save()
                    return JsonResponse(serializer.data, status=201)
        else:
            all_objects = []
            for d in data:
                serializer = WildSerializer(data=d, context={ 'request': Request(request) })
                if (serializer.is_valid()):
                    serializer.save()
                    all_objects.append(serializer.data)
                else:
                    return JsonResponse(serializer.errors, status=402)
            return JsonResponse({"objects": all_objects}, status=201)
        
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

        try: data['route']
        except: data['route'] = wild.route.id

        try: data['specie']
        except: data['specie'] = wild.specie.name

        try: data['probability']
        except: data['probability'] = wild.probability

        try: data['lvl']
        except: data['lvl'] = wild.lvl

        try: data['mode']
        except: data['mode'] = wild.mode

        try: data['time']
        except: data['time'] = wild.time

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
        data['associated_games'] = []
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
        return JsonResponse(serializer.data, status=201)

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
def accesses(request):
    if request.method == "GET":
        access = Access.objects.all()
        serializer = AccessSerializer(access, many=True, context={ 'request': Request(request) })
        return JsonResponse(serializer.data, safe=False)
    
    elif request.method == "POST":
        data = JSONParser().parse(request)
        data['routes'] = []
        serializer = AccessSerializer(data=data, context={ 'request': Request(request) })
        if (serializer.is_valid()):
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        
    return JsonResponse(serializer.errors, status=400)

@csrf_exempt
def accesses_detail(request, pk):
    try:
        access = Access.objects.get(pk=pk)
    except:
        return HttpResponse(status=404)
    
    if (request.method == 'GET'):
        serializer = AccessSerializer(access, context={ 'request': Request(request) })
        return JsonResponse(serializer.data, status=201)
    
    elif (request.method == 'PUT'):
        data = JSONParser().parse(request)
        serializer = AccessSerializer(access, data=data, context={ 'request': Request(request) })

        if (serializer.is_valid()):
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        
        return JsonResponse(serializer.errors, status=404)
    
    elif(request.method == 'DELETE'):
        access.delete()
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
                        'sprite': f'assets/sprites/{data['pokedex_id']}.png',
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
                "Places": {
                    1: [
                        [
                            "Route 1",
                            "Route 22",
                            "Route 2",
                            "Forêt de Jade"
                        ],
                        [
                            "Route 3",
                            "Route 4",
                            "Mont Sélénite - Rez-de-chaussée",
                            "Mont Sélénite - Sous-Sol 1",
                            "Mont Sélénite - Sous-Sol 2",
                            "Route 24",
                            "Route 25",
                        ],
                        [
                            "Route 5",
                            "Route 6",
                            "Route 11",
                            "Cave Taupiqueur"
                        ],
                        [
                            "Route 7",
                            "Route 8",
                            "Route 9",
                            "Route 10",
                            "Grotte - Rez-de-chaussée",
                            "Grotte - Sous-sol",
                            "Tour Pokémon - Etages 3 et 4",
                            "Tour Pokémon - Etage 5",
                            "Tour Pokémon - Etage 6",
                        ],
                        [
                            "Route 12",
                            "Route 13",
                            "Route 14",
                            "Route 15",
                            "Route 16",
                            "Route 17",
                            "Route 18",
                        ],
                        [
                            "Centrale",
                            "Chenal 19",
                            "Chenal 20",
                            "Îles Ecume - Rez-de-chaussée",
                            "Îles Ecume - Sous-Sol 1",
                            "Îles Ecume - Sous-Sol 2",
                            "Îles Ecume - Sous-Sol 3",
                            "Îles Ecume - Sous-Sol 4",
                            "Chenal 21",
                            "Route 23",
                        ],
                        [
                            "Route Victoire"
                        ],
                        [
                            "Grotte Inconnue"
                        ]
                    ],
                    2: [],
                    3: [
                        [
                            "Route 1",
                            "Route 22",
                            "Route 2",
                            "Forêt de Jade"
                        ],
                        [
                            "Route 3",
                            "Route 4",
                            "Mont Sélénite - Rez-de-chaussée",
                            "Mont Sélénite - Sous-Sol 1",
                            "Mont Sélénite - Sous-Sol 2",
                            "Route 24",
                            "Route 25",
                        ],
                        [
                            "Route 5",
                            "Route 6",
                            "Route 11",
                            "Cave Taupiqueur"
                        ],
                        [
                            "Route 7",
                            "Route 8",
                            "Route 9",
                            "Route 10",
                            "Grotte - Rez-de-chaussée",
                            "Grotte - Sous-sol",
                            "Tour Pokémon - Etages 3 et 4",
                            "Tour Pokémon - Etage 5",
                            "Tour Pokémon - Etage 6",
                        ],
                        [
                            "Route 12",
                            "Route 13",
                            "Route 14",
                            "Route 15",
                            "Route 16",
                            "Route 17",
                            "Route 18",
                        ],
                        [
                            "Centrale",
                            "Chenal 19",
                            "Chenal 20",
                            "Îles Ecume - Rez-de-chaussée",
                            "Îles Ecume - Sous-Sol 1",
                            "Îles Ecume - Sous-Sol 2",
                            "Îles Ecume - Sous-Sol 3",
                            "Îles Ecume - Sous-Sol 4",
                            "Chenal 21",
                            "Route 23",
                        ],
                        [
                            "Île Sevii 1 - Ville",
                            "Île Sevii 1 - Route Tison",
                            "Île Sevii 1 - Mont Braise - Extérieur",
                            "Île Sevii 1 - Mont Braise (Sommet) - Entrée et Sortie vers le sommet",
                            "Île Sevii 1 - Mont Braise (Sommet) - Caverne principale",
                            "Île Sevii 1 - Mont Braise (Rubis) - Entrée",
                            "Île Sevii 1 - Mont Braise (Rubis) - Sous-Sol 1",
                            "Île Sevii 1 - Mont Braise (Rubis) - Sous-Sol 2",
                            "Île Sevii 1 - Mont Braise (Rubis) - Sous-Sol 3",
                            "Île Sevii 2 - Cap Falaise",
                            "Île Sevii 3 - Pont du Lien",
                            "Île Sevii 3 - Bois Baies"
                        ],
                        [
                            "Route Victoire"
                        ],
                        [
                            "Île Sevii 1 - Plage Trésor",
                            "Île Sevii 3 - Port",
                        ],
                        [
                            "Île Sevii 4 - Ville",
                            "Île Sevii 4 - Grotte de Glace - Entrée",
                            "Île Sevii 4 - Grotte de Glace - Rez-de-chaussée",
                            "Île Sevii 4 - Grotte de Glace - Crique",
                            "Île Sevii 5 - Ville",
                            "Île Sevii 5 - Pré",
                            "Île Sevii 5 - Entrepôt Rocket",
                            "Île Sevii 5 - Mémorial",
                            "Île Sevii 5 - Labyrinthe d'O",
                            "Île Sevii 5 - Camp de Vacances",
                            "Île Sevii 5 - Grotte perdue - Salle sans objet",
                            "Île Sevii 5 - Grotte perdue - Salle avec objet",
                            "Île Sevii 6 - Ville",
                            "Île Sevii 6 - Agualcanal",
                            "Île Sevii 6 - Chemin Vert",
                            "Île Sevii 6 - Forbuissons",
                            "Île Sevii 6 - Grotte Métamo",
                            "Île Sevii 6 - Île du Lointain",
                            "Île Sevii 6 - Vallée Ruine",
                            "Île Sevii 7 - Ville",
                            "Île Sevii 7 - Canyon Sesor",
                            "Île Sevii 7 - Entrée Canyon",
                            "Île Sevii 7 - Ruines Tanoby",
                            "Île Sevii 7 - Tour Dresseurs",
                        ]
                    ],
                    4: [],
                    7: [],
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
                ],
            },
            "Johto": {
                "Places": {
                    2: [],
                    4: []
                },
                "Games": [
                    "Or",
                    "Argent",
                    "HeartGold",
                    "SoulSilver"
                ]
            },
            "Hoenn": {
                "Places": {
                    3: [],
                    6: []
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
                "Places": {
                    4: [],
                    8: []
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
                "Places": {
                    5: []
                },
                "Games": [
                    "Noir",
                    "Blanc",
                    "Noir 2",
                    "Blanc 2"
                ]
            },
            "Kalos": {
                "Places": {
                    6: []
                },
                "Games": [
                    "X",
                    "Y"
                ]
            },
            "Alola": {
                "Places": {
                    7: []
                },
                "Games": [
                    "Soleil",
                    "Lune",
                    "Ultra-Soleil",
                    "Ultra-Lune"
                ]
            },
            "Galar": {
                "Places": {
                    8: []
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
                    for i, places in enumerate(here["Places"][data_game["Game"].generation]):
                        for p in places:
                            data = {
                               "name": p,
                               "game_region": f"http://127.0.0.1:8000/api/games_regions/{data_game["Game Region"].id}/",
                               "access": i,
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

@csrf_exempt
def routes_from_game(request, game_id):
    if request.method == 'GET':
        datas = []
        game = Game.objects.get(id=game_id)
        games_regions = game.associated_regions.all()

        for gr in games_regions:
            routes_found = gr.routes.all()
            for r in routes_found:
                datas.append(r)
        
        serializer = RouteSerializer(datas, many=True, context={ 'request': Request(request) })
        return JsonResponse(serializer.data, safe=False)
        
    return JsonResponse(serializer.errors, status=400)