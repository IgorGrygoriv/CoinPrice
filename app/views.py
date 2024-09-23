from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import requests
import logging
import pandas as pd
from .config import api_key

def landingPage(request):
    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {
        'ids': 'bitcoin,ethereum,cardano',
        'vs_currencies': 'usd',
        'include_24hr_change': 'true',
    }
    headers = {
        "accept": "application/json",
        "x-cg-demo-api-key": api_key,
    }
    response = requests.get(url, headers=headers, params=params)
    data = []        

    if response.status_code == 200:
        data = response.json()

    return render(request, "app/index.html", {"data": data})

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
                "image": coin["image"],
            }
            data.append(filtered_data)
    return render(request, "app/home.html", {"data": data})

def crypto_details(request):
   if request.method == "POST":
        coin_id = request.POST.get('coin_id')

        url = f"https://api.coingecko.com/api/v3/coins/" + coin_id
        historical_data_url = f"https://api.coingecko.com/api/v3/coins/" + coin_id + "/ohlc"
        headers = {
            "accept": "application/json",
            "x-cg-demo-api-key": api_key,
        }
        params = {
            'vs_currency': 'usd',
            'days': '14',
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
                "image": coin["image"]["large"],
            }

            historical_data_response = requests.get(historical_data_url, headers=headers, params=params)
            if historical_data_response.status_code == 200:
                ohlc_data = historical_data_response.json()

                ohlc_formatted = {
                    'date': [pd.to_datetime(entry[0], unit='ms').strftime('%Y-%m-%d') for entry in ohlc_data],  
                    'open': [entry[1] for entry in ohlc_data], 
                    'high': [entry[2] for entry in ohlc_data], 
                    'low': [entry[3] for entry in ohlc_data],  
                    'close': [entry[4] for entry in ohlc_data]  
                }


            response_data = {
                'filtered_data': filtered_data,
                'ohlc_data': ohlc_formatted
            }

            return JsonResponse(response_data)
        else:
            return JsonResponse({'error': 'Coin not found or API error.'}, status=400)

def login(request):
    return render(request, "app/login.html")

def register(request):
    return render(request, "app/register.html")
