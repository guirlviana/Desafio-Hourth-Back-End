from django.http import JsonResponse
from django.shortcuts import render
import requests
from api.utils import valider_dates, format_to_date

response_for_challenge = []

def update_project(brute_product):
    product = brute_product
    has_register = False

    for prod in response_for_challenge:
        if prod['product_url'] == product['product_url']:
            prod[product['consult_date']] = product['vendas_no_dia']
            prod['total_sales'] += product['vendas_no_dia']
            has_register = True
            break
        
    if not has_register:
        response_for_challenge.append({
            "product_url__image":product['product_url__image'],
            "product_url":product['product_url'],
            "product_url__created_at":product['product_url__created_at'],
            "total_sales": 0, 
        })
        update_project(product)

def index(request):
    initial_date = request.GET.get('initial_date')
    finish_date = request.GET.get('finish_date')
    status = valider_dates(initial_date, finish_date)
    
    data = requests.get('https://mc3nt37jj5.execute-api.sa-east-1.amazonaws.com/default/hourth_desafio')
    response = data.json()
    response_for_challenge.clear()
    
    if status['status']:
        
        if(status['filter']):
            for product in response:
                product_date = format_to_date(product['consult_date'])
                if (status['date_initial'] <= product_date <= status['date_finish']):
                    update_project(product)
                
        else:
            [update_project(product) for product in response]

        return JsonResponse(response_for_challenge, safe=False, status=200)
    return JsonResponse(status, status=400)

def table(request):
    result = index(request)
    return render(request, 'templates/table.html', {result: result})
