# parsing data from the client
from rest_framework.parsers import JSONParser
from rest_framework.request import Request
# To bypass having a CSRF token
from django.views.decorators.csrf import csrf_exempt
# for sending response to the client
from django.http import HttpResponse, JsonResponse
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