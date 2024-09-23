from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import requests
import logging
from .config import api_key

def landingPage(request):
    return render(request, "app/index.html")

def homepage(request):
    url = "https://api.coingecko.com/api/v3/coins/markets"
    headers = {
        "accept": "application/json",
        "x-cg-demo-api-key": api_key,
        
    }
    params = {
        'vs_currency': 'usd',        
        'order': 'market_cap_desc',               
        'per_page': 10,                           
        'page': 1,                                
        'sparkline': 'false',                     
        'price_change_percentage': '24h'          
    }
    response = requests.get(url, headers=headers, params=params)
    data =[]
    if response.status_code == 200:
        full_data = response.json()
        for coin in full_data:
            filtered_data = {
                "id": coin["id"],
                "name": coin["name"],
                "symbol": coin["symbol"],
                "current_price": coin["current_price"],
                "price_change_24h": coin["price_change_24h"],
                "price_change_percentage_24h": coin["price_change_percentage_24h"],
                "high_24h": coin["high_24h"],
                "low_24h": coin["low_24h"],
            }
            data.append(filtered_data)
    return render(request, "app/home.html", {"data": data})

def crypto_details(request):
   if request.method == "POST":
        coin_id = request.POST.get('coin_id')

        url = f"https://api.coingecko.com/api/v3/coins/" + coin_id
        headers = {
            "accept": "application/json",
            "x-cg-demo-api-key": api_key,
        }

        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            coin = response.json()
            filtered_data = {
                "id": coin.get("id"),
                "name": coin.get("name"),
                "symbol": coin.get("symbol"),
                "current_price": coin["market_data"]["current_price"]["usd"],
                "price_change_24h": coin["market_data"].get("price_change_24h"),
                "price_change_percentage_24h": coin["market_data"].get("price_change_percentage_24h"),
                "high_24h": coin["market_data"]["high_24h"]["usd"],
                "low_24h": coin["market_data"]["low_24h"]["usd"],
            }
            return JsonResponse(filtered_data)
        else:
            return JsonResponse({'error': 'Coin not found or API error.'}, status=400)


def login(request):
    return render(request, "app/login.html")

def register(request):
    return render(request, "app/register.html")
